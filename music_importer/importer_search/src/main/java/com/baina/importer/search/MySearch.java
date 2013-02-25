package com.baina.importer.search;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.lang.StringUtils;
import org.apache.log4j.Logger;
import org.apache.lucene.analysis.SimpleAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.Field.Index;
import org.apache.lucene.document.Field.Store;
import org.apache.lucene.index.CorruptIndexException;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.MultiReader;
import org.apache.lucene.queryParser.ParseException;
import org.apache.lucene.queryParser.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

import com.baina.importer.search.bean.MetaBean;
import com.baina.importer.search.common.Denoiser;
import com.baina.importer.search.common.ProConfig;
import com.baina.importer.search.common.StringUtil;

/**
 * Hello world!
 * 
 */
public class MySearch {
    private static Logger logger = Logger.getLogger(LuceneTest.class);
    
    private final static MySearch mySearch = new MySearch();;

    private FSDirectory directory = null;

    private IndexWriter writer = null;

    private IndexReader RTReader = null;
    private IndexReader FSReader = null;

    private IndexSearcher searcher = null;

    private final int MaxBufferedDocs = 100000;
    private final double RAMBufferSizeMB = 256;
    private final int MaxCommitCount = 200;

    private long lastCommitCount = 0L;
    private long lastCommitTime = 0L;
    private final int commitInterval = 2 * 60 * 1000;

    private MySearch() {
        try {
            directory = FSDirectory.open(new File(ProConfig.Default
                    .getProperty("index.folder")));

            writer = new IndexWriter(directory, new SimpleAnalyzer(), true,
                    IndexWriter.MaxFieldLength.UNLIMITED);

            writer.setRAMBufferSizeMB(RAMBufferSizeMB);
            writer.setMaxBufferedDocs(MaxBufferedDocs);

            lastCommitCount = writer.numDocs();

            RTReader = IndexReader.open(writer, true);
            try {
                FSReader = IndexReader.open(directory);
            } catch (IOException e) {
                logger.error("", e);
            }
        } catch (IOException e) {
            logger.error("", e);
        }
    }

    public static MySearch getInstance() {
        return mySearch;
    }

    public void addDoc(MetaBean meta) throws CorruptIndexException, IOException {
        Document doc = new Document();

        doc.add(new Field("song_id", meta.song_id + "", Store.YES,
                Index.NOT_ANALYZED_NO_NORMS));

        StringBuilder sb = new StringBuilder();
        append(sb, meta.artist_name, 1);
        append(sb, meta.album_name, 1);
        append(sb, meta.name, 1);

        doc.add(new Field("ft", sb.toString(), Store.NO, Index.ANALYZED));

        doc.add(new Field("name", meta.name, Store.YES,
                Index.NOT_ANALYZED_NO_NORMS));
        doc.add(new Field("artist_name", meta.artist_name, Store.YES,
                Index.NOT_ANALYZED_NO_NORMS));
        doc.add(new Field("album_name", meta.album_name, Store.YES,
                Index.NOT_ANALYZED_NO_NORMS));

        writer.addDocument(doc);

        if (writer.numDocs() > (lastCommitCount + MaxCommitCount)) {
            commitRAMdata();
        }

    }

    public List<MetaBean> search(String queryStr) throws CorruptIndexException,
            IOException, ParseException {
        List<MetaBean> metas = new ArrayList<MetaBean>();

        reopenReaderIfNecessary();

        List<IndexReader> readers = new ArrayList<IndexReader>();

        readers.add(RTReader);

        if (FSReader != null) {
            readers.add(FSReader);
        }

        searcher = new IndexSearcher(new MultiReader(
                readers.toArray(new IndexReader[readers.size()]), true));

        String keyword = StringUtil.simpleHandle(queryStr);

        keyword = Denoiser.processPunc(keyword);
        keyword = Denoiser.process(keyword);

        keyword = Denoiser.processRepetitions(keyword);

        if (StringUtils.isEmpty(keyword)) {
            return metas;
        }

        String[] terms = keyword.split("\\s+");
        keyword = "";
        for (String term : terms) {
            keyword += "+" + term + " ";
        }
        QueryParser parser = new QueryParser(Version.LUCENE_36, "ft",
                new SimpleAnalyzer());
        Query query = parser.parse(keyword);

        TopDocs rs = searcher.search(query, null, 10);

        for (ScoreDoc d : rs.scoreDocs) {
            Document hitDoc = searcher.doc(d.doc);
            MetaBean meta = MetaBean.getAudioBean(hitDoc);
            metas.add(meta);
        }

        return metas;
    }

    private void reopenReaderIfNecessary() throws IOException {
        IndexReader newRTReader = IndexReader.openIfChanged(RTReader);

        if (newRTReader != null) {
            RTReader.close();
            RTReader = newRTReader;
        }

        return;
    }

    private void append(StringBuilder sb, String s, int times) {
        if (StringUtils.isEmpty(s)) {
            return;
        }

        s = Denoiser.processPunc(s);
        s = Denoiser.process(s);

        for (int i = 0; i < times; ++i) {
            sb.append(" " + s);
        }
    }

    public void commitRAMdata() throws CorruptIndexException, IOException {
        long nowTime = System.currentTimeMillis();
        if ((nowTime - lastCommitTime) > commitInterval
                && lastCommitCount != writer.numDocs()) {
            writer.commit();
            lastCommitCount = writer.numDocs();
            lastCommitTime = System.currentTimeMillis();
            System.out.println("commit using time: "
                    + (lastCommitTime - nowTime));
        }
    }
}
