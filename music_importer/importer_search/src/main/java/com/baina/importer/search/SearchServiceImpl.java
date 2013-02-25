package com.baina.importer.search;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.apache.lucene.index.CorruptIndexException;
import org.apache.lucene.queryParser.ParseException;
import org.apache.thrift.TException;

import com.baina.importer.search.bean.MetaBean;
import com.baina.importer.search.service.thrift.Meta;
import com.baina.importer.search.service.thrift.ResultCode;
import com.baina.importer.search.service.thrift.SearchService;

public class SearchServiceImpl implements SearchService.Iface {

    public List<Meta> search(String query) throws TException {
        List<Meta> metaResult = new ArrayList<Meta>();
        List<MetaBean> metas = null;
        
        MySearch mySearch = MySearch.getInstance();
       
        try {
            metas = mySearch.search(query);
        } catch (CorruptIndexException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }
        
        
        for (MetaBean metaBean : metas) {
            Meta meta = new Meta();
            meta.song_id = metaBean.song_id;
            meta.name = metaBean.name;
            meta.album_name = metaBean.album_name;
            meta.artist_name = metaBean.artist_name;
            metaResult.add(meta);
        }
        
        return metaResult;
    }

    public ResultCode addDoc(Meta meta) throws TException {
        MetaBean metaBean = new MetaBean();
        metaBean.name = meta.name;
        metaBean.artist_name = meta.artist_name;
        metaBean.album_name = meta.album_name;
        metaBean.song_id = meta.song_id;
        
        MySearch mySearch = MySearch.getInstance();
        
        try {
            mySearch.addDoc(metaBean);
        } catch (CorruptIndexException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        return ResultCode.SUCCESS;
    }

}
