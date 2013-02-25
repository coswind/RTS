package com.baina.importer.search.bean;

import org.apache.commons.lang.NumberUtils;
import org.apache.lucene.document.Document;

import com.google.common.base.Strings;

public class MetaBean {
    public int song_id;

    public String name;

    public String artist_name = "";

    public String album_name = "";

    public static MetaBean getAudioBean(Document doc) {

        MetaBean meta = new MetaBean();
        
        meta.song_id = NumberUtils.stringToInt(doc.get("song_id"));
        
        meta.name = Strings.nullToEmpty(doc.get("name"));
        meta.artist_name = Strings.nullToEmpty(doc.get("artist_name"));
        meta.album_name = Strings.nullToEmpty(doc.get("album_name"));
        
        return meta;
    }
}