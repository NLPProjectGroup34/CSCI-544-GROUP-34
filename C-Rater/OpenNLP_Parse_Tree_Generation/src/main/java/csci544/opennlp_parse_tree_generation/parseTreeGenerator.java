/**
 *
 * @author Dipali Bhatt
 */
package csci544.opennlp_parse_tree_generation;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.logging.Level;
import java.util.logging.Logger;
import opennlp.tools.cmdline.parser.ParserTool;
import opennlp.tools.parser.Parse;
import opennlp.tools.parser.Parser;
import opennlp.tools.parser.ParserFactory;
import opennlp.tools.parser.ParserModel;
import opennlp.tools.util.InvalidFormatException;

public class parseTreeGenerator {
    
    public static void main(String []args) {
        try {
            Parse(args[0]);
        } catch (IOException ex) {
            Logger.getLogger(parseTreeGenerator.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
    public static void Parse(String sentence) throws InvalidFormatException, IOException {
	// http://sourceforge.net/apps/mediawiki/opennlp/index.php?title=Parser#Training_Tool
	InputStream is = new FileInputStream("E:\\USC\\CSCI-544\\Project\\Automated Grading\\C-Rater\\OpenNLP_Parse_Tree_Generation\\target\\classes\\opennlp-models\\opennlp\\tools\\parser\\en-parser-chunking.bin");
 
	ParserModel model = new ParserModel(is);
 
	Parser parser = ParserFactory.create(model);
 
	Parse topParses[] = ParserTool.parseLine(sentence, parser, 1);
 
	for (Parse p : topParses)
		p.show();
 
	is.close();
 
	/*
	 * (TOP (S (NP (NN Programcreek) ) (VP (VBZ is) (NP (DT a) (ADJP (RB
	 * very) (JJ huge) (CC and) (JJ useful) ) ) ) (. website.) ) )
	 */
}
    
}
