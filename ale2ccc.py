#!/usr/bin/env python
"""
Extracts ASC CDL information from an AvidLogExchange file and writes into a
color correction collection file.

Usage: %prog infile.ale outfile.ccc

The variable NAMING_CONVENTION_REGEX contains the regex used to create an id
attribute for each of the ColorCorrections contained in the collection.

If the ALE file does not contain Columns named ASC_SOP and ASC_SAT the extract
will fail. Files which do not match the regex are warned and skipped over.

Example Color Correction Collection file:

<ColorCorrectionCollection xmlns="urn:ASC:CDL:v1.2">
      <ColorCorrection id="af-123">
              <SOPNode>
                   <Slope>2 1 1</Slope>
                   <Offset>0 0 0</Offset>
                   <Power>1 1 1</Power>
              </SOPNode>
              <SATNode>
                   <Saturation>1</Saturation>
              </SATNode>
        </ColorCorrection>
        <ColorCorrection id="mygrade">
                <SOPNode>
                     <Slope>0.9 0.7 0.9</Slope>
                     <Offset>0 0 0</Offset>
                     <Power>1 1 1</Power>
                </SOPNode>
                <SATNode>
                     <Saturation>1</Saturation>
                </SATNode>
          </ColorCorrection>
</ColorCorrectionCollection>
"""


import os
import sys
from xml.dom import minidom
import re
import traceback

NAMING_CONVENTION_REGEX = '^(\d+\w\w_\d+)'

class ColorCorrectionList(object):
    def __init__(self):
        self.dom = minidom.parseString('<ColorCorrectionCollection xmlns="urn:ASC:CDL:v1.2"></ColorCorrectionCollection>')
        object.__init__(self)

    def ColorCorrection(self, id, slope, offset, power, saturation):
        """
        Parameters:
            id = Str
            slope = tuple(float, float, float)
            offset = tuple(float, float, float)
            power = tuple(float, float, float)
            saturation = float
        """

        #slope = (1.1583, 0.8242, 0.8109)
        #offset = (-0.0064, 0.0287, 0.0448)
        #power = (0.7710, 0.9064, 1.0039)
        #saturation = 1.7000 

        # Start of ColorCorrection
        cc = self.dom.createElement('ColorCorrection')
        cc.attributes['id'] = id
        self.dom.childNodes[0].appendChild(cc)

        # SOP
        SOP_node = self.dom.createElement('SOPNode')
        cc.appendChild(SOP_node)

        slope_text = self.dom.createTextNode(" ".join(slope))
        slope_node = self.dom.createElement('Slope')
        slope_node.appendChild(slope_text)

        offset_text = self.dom.createTextNode(" ".join(offset))
        offset_node = self.dom.createElement('Offset')
        offset_node.appendChild(offset_text)

        power_text = self.dom.createTextNode(" ".join(power))
        power_node = self.dom.createElement('Power')
        power_node.appendChild(power_text)

        SOP_node.appendChild(slope_node)
        SOP_node.appendChild(offset_node)
        SOP_node.appendChild(power_node)

        # SAT
        SAT_node = self.dom.createElement('SATNode')
        cc.appendChild(SAT_node)

        saturation_text = self.dom.createTextNode(saturation)
        saturation_node = self.dom.createElement('Saturation')
        saturation_node.appendChild(saturation_text)

        SAT_node.appendChild(saturation_node)

    def __str__(self):
        return self.dom.toprettyxml()

# the first argument to the script is the input file, the second argument is the output file.
if len(sys.argv) != 3:
    raise Exception('Invalid number of arguments. Usage: %prog infile.ale outfile.ccc')

ale_file = sys.argv[1]
ccc_file = sys.argv[2]

color_collection = ColorCorrectionList()

with open(ale_file) as fp:
    for line in iter(fp.readline, ''):
        try:
            line_tokens = re.split('[\t]', line.strip())
            #print line_tokens

            if line_tokens[0] == "Column":
                nextline = fp.readline()
                NAME_POS = [i for i,x in enumerate(re.split('[\t]', nextline)) if x == 'Name'][0]
                ASC_SOP_POS = [i for i,x in enumerate(re.split('[\t]', nextline)) if x == 'ASC_SOP'][0]
                ASC_SAT_POS = [i for i,x in enumerate(re.split('[\t]', nextline)) if x == 'ASC_SAT'][0]

            if line_tokens[0] == "Data":
                for data in iter(fp.readline, ''):
                    fields = re.split('[\t]', data)
                    
                    try:
                        id = re.findall(NAMING_CONVENTION_REGEX, fields[NAME_POS])[0]
                    except:
                        print "turnover item %s does not match naming convention!" % fields[NAME_POS]

                    sop_tokens = re.findall('\d+\.\d+', fields[ASC_SOP_POS])
                    saturation = fields[ASC_SAT_POS]

                    slope = sop_tokens[0:3]
                    offset = sop_tokens[3:6]
                    power = sop_tokens[6:9]
                    
                    color_collection.ColorCorrection(id, slope, offset, power, saturation)

        except Exception as e:
            # catch all for any dodgy formatted lines.
            traceback.print_exc()
            print e
             
        
with open(ccc_file, 'w') as fp:
    fp.write(str(color_collection))
