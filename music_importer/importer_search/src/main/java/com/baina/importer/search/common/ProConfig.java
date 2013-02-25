package com.baina.importer.search.common;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class ProConfig {
    private Properties properties = new Properties();
    public static ProConfig Default = new ProConfig("/pro.properties");

    public ProConfig(String configPath) {
        try {
            InputStream i = ProConfig.class.getResourceAsStream(configPath);

            if(i != null) {
                properties.load(i);
                i.close();
            }

        } catch(IOException e) {
        }
    }

    public Properties getProperties() {
        return properties;
    }

    public String getProperty(String name) {
        return properties.getProperty(name);
    }

    public int getInt(String name) {
        return getInt(name, 0);
    }

    public int getInt(String name, int defVal) {
        int ret = defVal;

        try {
            ret = Integer.parseInt(properties.getProperty(name));

        } catch(Exception e) {

        }

        return ret;
    }

    public long getLong(String name) {
        return getLong(name, 0L);

    }

    public long getLong(String name, long defVal) {
        long ret = defVal;

        try {
            ret = Long.parseLong(properties.getProperty(name));

        } catch(Exception e) {

        }

        return ret;

    }

    public boolean getBoolean(String name) {
        return getBoolean(name, false);

    }

    public boolean getBoolean(String name, boolean defVal) {
        boolean ret = defVal;

        try {
            ret = Boolean.parseBoolean(properties.getProperty(name));

        } catch(Exception e) {

        }

        return ret;

    }
}