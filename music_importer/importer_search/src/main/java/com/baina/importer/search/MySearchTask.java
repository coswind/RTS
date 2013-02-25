package com.baina.importer.search;

import java.io.IOException;
import java.util.TimerTask;

import org.apache.lucene.index.CorruptIndexException;

public class MySearchTask extends TimerTask {

    @Override
    public void run() {
        MySearch mySearch = MySearch.getInstance();
        try {
            mySearch.commitRAMdata();
        } catch (CorruptIndexException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
