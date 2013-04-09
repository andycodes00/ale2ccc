# ale2ccc

Extract ASC CDL grades from an AvidLogExchange (ALE) file and write out to an ASC ColorCorrectionCollection (CCC)

My 5 minutes of searching online for a script to do this already proved fruitless. So I threw this together. Its not pretty, but it gets the job done. 

## Usage

    %prog infile.ale outfile.ccc

* The variable NAMING_CONVENTION_REGEX contains the regex used to create an id
attribute for each of the ColorCorrections contained in the collection.

* If the ALE file does not contain Columns named ASC_SOP and ASC_SAT the extract
will fail. 

* Files which do not match the regex are warned and skipped over.

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

