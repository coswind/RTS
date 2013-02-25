
package com.baina.importer.search.common;

import org.apache.commons.lang.StringUtils;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Iterator;
import java.util.List;

public class StringUtil {

    private static SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");


    public static boolean hasHanzi(String str) {

        if(str == null || str.length() == 0) {
            return false;
        }

        for(int i = 0; i < str.length(); ++i) {
            if(isHanzi(str.charAt(i))) {
                return true;
            }

        }

        return false;
    }

    public static boolean isHanzi(char c) {

        return c >= '\u4e00' && c <= '\u9fa5';
    }

    public static boolean isJapanese(char c) {

        return c >= '\u3040' && c <= '\u32ff';
    }

    public static boolean hasJapanese(String str) {

        if(StringUtils.isEmpty(str)) {
            return false;
        }

        for(int i = 0; i < str.length(); ++i) {
            if(isJapanese(str.charAt(i))) {
                return true;
            }

        }

        return false;
    }

    public static boolean isMeaningful(char c) {

        if(c >= '0' && c <= '9' || c >= 'a' && c <= 'z' || isHanzi(c) || isJapanese(c) || c == ' '
           || c == '·') {
            return true;
        }

        return false;
    }

    public static String getMeaningful(String string) {

        StringBuilder sb = new StringBuilder();

        for(int i = 0; i < string.length(); ++i) {
            char c = string.charAt(i);

            if(isMeaningful(c)) {
                sb.append(c);

            } else {
                sb.append(' ');
            }
        }

        return sb.toString();
    }

    public static String ensureNotNull(String s) {

        return s == null ? "" : s.trim();
    }

    public static boolean exists(List<String> list, String append, boolean ignoreCase) {

        if(append == null || append.length() == 0 || list == null || list.size() == 0) {
            return false;
        }

        for(String s : list) {
            if(ignoreCase) {
                if(append.equalsIgnoreCase(s)) {
                    return true;
                }

            } else {
                if(append.equals(s)) {
                    return true;
                }
            }
        }

        return false;

    }

    public static boolean remove(List<String> list, String append, boolean ignoreCase,
                                 boolean removeAll) {

        if(append == null || append.length() == 0 || list == null || list.size() == 0) {
            return false;
        }

        boolean ret = false;
        Iterator<String> itr = list.iterator();

        while(itr.hasNext()) {
            String s = itr.next();

            if(ignoreCase) {
                if(s.equalsIgnoreCase(append)) {
                    itr.remove();
                    ret = true;

                    if(!removeAll) {
                        break;
                    }
                }

            } else {
                if(s.equals(append)) {
                    itr.remove();
                    ret = true;

                    if(!removeAll) {
                        break;
                    }
                }
            }

        }

        return ret;

    }

    public static boolean addIfNotExists(List<String> list, String append, boolean ignoreCase) {

        if(append == null || append.length() == 0 || list == null) {
            return false;
        }

        boolean exist = exists(list, append, ignoreCase);

        if(!exist) {
            list.add(append);
            return true;
        }

        return false;

    }

    public static String simpleHandle(String keyword) {

        keyword = keyword.toLowerCase();
        keyword = StringUtils.stripToEmpty(keyword);
        keyword = keyword.replace("\r\n", " ");
        keyword = keyword.replace("\n", " ");
        keyword = StringUtil.getMeaningful(keyword);

        StringBuilder sb = new StringBuilder();
        int length = keyword.length();

        for(int i = 0; i < length;) {
            char c = keyword.charAt(i);
            sb.append(c);
            ++i;

            if(c == ' ') {
                while(i < length && keyword.charAt(i) == ' ') {
                    ++i;
                }
            }
        }

        return sb.toString();
    }



    public static long tryParseTime(String str) {

        return tryParseTime(str, 0);
    }

    public static long tryParseTime(String str, long defaultValue) {

        if(str == null) {
            return defaultValue;
        }

        try {
            return format.parse(str).getTime();

        } catch(ParseException e) {
        }

        return defaultValue;
    }

    public static String formatTime(long time) {

        return format.format(new Date(time));
    }

}
