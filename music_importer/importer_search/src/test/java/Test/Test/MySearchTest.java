package Test.Test;

import java.io.IOException;
import java.util.List;

import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;

import org.apache.lucene.index.CorruptIndexException;
import org.apache.lucene.queryParser.ParseException;

import com.baina.importer.search.MySearch;
import com.baina.importer.search.bean.MetaBean;

/**
 * Unit test for simple App.
 */
public class MySearchTest extends TestCase {
    /**
     * Create the test case
     * 
     * @param testName
     *            name of the test case
     */
    public MySearchTest(String testName) {
        super(testName);
    }

    /**
     * @return the suite of tests being tested
     */
    public static Test suite() {
        return new TestSuite(MySearchTest.class);
    }

    /**
     * Rigourous Test :-)
     * 
     * @throws IOException
     * @throws CorruptIndexException
     * @throws ParseException 
     */
    public void testMySearch() throws CorruptIndexException, IOException, ParseException {
        MetaBean meta = new MetaBean();
        meta.song_id = 1;
        meta.name = "落花";
        meta.artist_name = "潘越云";
        meta.album_name = "精选辑(一)";
        
        MySearch mySearch = MySearch.getInstance();
       
        for (int i = 0; i < 100; i++) {
            meta.album_name = "精选辑(一)" + i;
//            mySearch.addDoc(meta);

            List<MetaBean> results = null;
            results = mySearch.search(meta.album_name + i);
            for (MetaBean result : results) {
                System.out.println(result.album_name);
                break;
            }
        }
        
//        mySearch.commitRAMdata();
        /*String keyword = "潘越云 精选辑(一) 落花";
        keyword = Denoiser.processPunc(keyword);
        System.out.println(keyword);
        keyword = Denoiser.process(keyword);
        System.out.println(keyword);*/

        assertTrue(true);
    }
}
