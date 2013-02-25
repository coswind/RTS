package com.baina.importer.search;

import java.io.IOException;
import java.io.StringReader;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.cn.smart.SmartChineseAnalyzer;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.queryParser.ParseException;
import org.apache.lucene.util.Version;

public class LuceneTest {
    
    public static void main(String[] args) throws IOException, ParseException {
        /*
         * FSDirectory directory = FSDirectory.open(new File("/tmp/data")); int
         * numCount = 0; IndexWriter writer = new IndexWriter(directory, new
         * SimpleAnalyzer(), true, IndexWriter.MaxFieldLength.UNLIMITED);
         * 
         * IndexReader RTReader = IndexReader.open(writer, true);
         * 
         * Document doc = new Document(); doc.add(new Field("partnum",
         * "夏毅 夏毅 ccoswind", Field.Store.YES, Field.Index.ANALYZED));
         * doc.add(new Field("description", "Illidium Space Modulator",
         * Field.Store.YES, Field.Index.ANALYZED)); writer.addDocument(doc);
         * 
         * numCount = writer.numDocs();
         * 
         * if (numCount != writer.numDocs()) { writer.commit(); numCount =
         * writer.numDocs(); }
         * 
         * long start = System.currentTimeMillis();
         * 
         * IndexReader newRTReader = IndexReader.openIfChanged(RTReader);
         * 
         * if (newRTReader != RTReader) { RTReader.decRef();
         * System.out.println("decRef---" + RTReader.getRefCount()); RTReader =
         * newRTReader; }
         * 
         * List<IndexReader> readers = new ArrayList<IndexReader>();
         * 
         * readers.add(RTReader);
         * 
         * try { IndexReader FSReader = IndexReader.open(directory); if
         * (FSReader != null) { readers.add(FSReader); } } catch(IOException e)
         * { }
         * 
         * IndexSearcher searcher = new IndexSearcher(new
         * MultiReader(readers.toArray(new IndexReader[readers.size()]), true));
         * QueryParser queryParser = new QueryParser(Version.LUCENE_36,
         * "partnum", new SimpleAnalyzer());
         * 
         * Query query = queryParser.parse("+夏毅 +ccoswind"); TopDocs rs =
         * searcher.search(query, null, 10); System.out.println(rs.totalHits);
         * 
         * if (rs.scoreDocs.length > 0) { Document firstHit =
         * searcher.doc(rs.scoreDocs[0].doc);
         * System.out.println(firstHit.get("description")); }
         * 
         * 
         * searcher.close(); System.out.println(System.currentTimeMillis() -
         * start);
         */
        // MySearch mySearch = MySearch.getInstance();

        Analyzer analyzer = new SmartChineseAnalyzer(Version.LUCENE_36);
        String[] texts = new String[] { "小明把大便当作每天早上起床第一件要做的事" };
        
        for (String s : texts) {
            TokenStream tokeStream = analyzer.tokenStream("content", new StringReader(s));
            // TermAttribute 已过时，文档中推荐使用CharTermAttribute
            tokeStream.addAttribute(CharTermAttribute.class);
            System.out.println("------------Test----------");
            while (tokeStream.incrementToken()) {
                
                CharTermAttribute ta = tokeStream
                        .getAttribute(CharTermAttribute.class);
                System.out.println(ta.toString());
                // System.out.println(tokeStream.toString());
            }
        }
        
        analyzer.close();
    }
}