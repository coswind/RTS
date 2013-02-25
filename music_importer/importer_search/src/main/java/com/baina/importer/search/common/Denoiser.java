/**
 *
 */
package com.baina.importer.search.common;

import org.apache.commons.lang.StringUtils;

import java.util.HashSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

//对输入的查询项去噪音，然后送入查询分析器
public class Denoiser {
    private static final String[] extensions = new String[] {
        "jpg", "gif", "mp3", "mp4", "avi", "wav", "aiff", "aif", "au", "snd", "voc", "ra",
        "ram", "mid", "rm", "mod", "s3m", "rmvb"
    };
    private static HashSet<String> extMap = new HashSet<String>(extensions.length, 0.75f);
    static {
        for(String s : extensions) {
            extMap.add(s);
        }

    }

    public static String process(String input) {

        // DO not do aggressive processing.Just remove redundant white
        // characters and turn into simplified Chinese.

        if(StringUtils.isEmpty(input)) {
            return input;
        }

        String res = processWhite(input);
        res = processCapital(res);
        String[] strings = res.split("\\s");

        if(strings == null || strings.length == 0) {
            return "";
        }

        for(int i = 0; i < strings.length; ++i) {
            strings[i] = processChinese(strings[i]);
        }

        StringBuilder sb = new StringBuilder(strings.length);

        for(int i = 0; i < strings.length; ++i) {
            String temp = strings[i];

            /*if(!StringUtil.hasHanzi(temp) || temp.length() > 1) {
                sb.append(temp).append(' ');

            } else {
                if(StringUtil.hasHanzi(temp) && temp.length() == 1
                   && sb.length() > 0
                   && sb.charAt(sb.length() - 1) == ' ') {
                    sb.deleteCharAt(sb.length() - 1);
                }

                sb.append(temp);
            }*/
            
            sb.append(temp).append(' ');

        }

        return sb.toString().trim();
    }

    private static Pattern pWhite = Pattern.compile("\\s+");

    public static String processWhite(String input) {

        input = StringUtils.stripToEmpty(input);

        if(StringUtils.isEmpty(input)) {
            return input;
        }


        Matcher matcher = pWhite.matcher(input);
        return matcher.replaceAll(" ");

    }

    public static String processCapital(String input) {

        return input.toLowerCase();
    }

    // 带后缀名的搜索项，过滤掉后缀名，例如搜索“乱世佳人.mp4”简化为“乱世佳人“
    public static String processExtension(String input) {

        int i = input.lastIndexOf('.');

        if(i == 0 && input.length() > 1) {
            return input.substring(1);
        }

        if(i > 0 && i < input.length() - 1) {
            String ext = input.substring(i + 1);

            if(extMap.contains(ext)) {
                input = input.substring(0, i);
            }
        }

        return input;
    }

    // 去除标点符号和处理特殊符号，去除's，é转e
    public static String processPunc(String input) {

        if(StringUtils.isEmpty(input)) {
            return input;
        }

        input = input.replace("'s", "");
        StringBuilder sb = new StringBuilder(input.length());

        for(int i = 0; i < input.length(); ++i) {
            char c = input.charAt(i);

            if(c == 'á' || c == 'à') {
                c = 'a';

            } else if(c == 'ê' || c == 'è' || c == 'é') {
                c = 'e';

            } else if(c == 'ó' || c == 'ò') {
                c = 'o';

            } else if(c == '@' || c == ',' || c == '.' || c == '&' || c == '%' || c == '$'
                      || c == '\'' || c == '+' || c == '-' || c == '《' || c == '》' || c == '<'
                      || c == '>' || c == '*' || c == '/' || c == '^' || c == '(' || c == ')'
                      || c == '[' || c == ']' || c == '{' || c == '}') {
                c = ' ';
            }


            sb.append(c);
        }

        return sb.toString();

    }

    // 把重复的字符串压缩，例如用户输入“快快快快”
    public static String processRepetitions(String input) {

        if(StringUtils.isEmpty(input)) {
            return input;
        }

        StringBuilder sb = new StringBuilder(input.length());
        char old = 0;
        int count = 0;

        for(int i = 0; i < input.length(); ++i) {
            char c = input.charAt(i);

            if(c == old) {
                count++;

                if(count < 3) {
                    sb.append(c);
                }

            } else {
                old = c;
                sb.append(c);
            }
        }

        return sb.toString();
    }

    // 繁体转简体，全角转半角
    public static String processChinese(String input) {

        return Chars.getSimple(input);
    }

}
