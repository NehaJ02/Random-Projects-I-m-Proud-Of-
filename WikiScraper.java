/*
* AUTHOR: Neha Joshi
* FILE: WikiScraper.java
* ASSIGNMENT: Programming Assignment 
* COURSE: CSc 210; Section 001; Spring 2022
* PURPOSE: This program takes in the passed in wiki link name and looks for any
* 		   any wiki pages found in its html source code. It also implements
* 		   memoization using a ConcurrentHashMap, which is more thread-safe,
* 		   to keep track of any pages who have already been searched so that
* 		   the expensive task of opening the url and accessing the internet
* 		   repeatedly doesn't have to happen and the site doesn't throw a 429 error
* 		   as fast on the user.
* 
*/

import java.io.InputStream;
import java.net.URL;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

public class WikiScraper {
	
	public static Map<String, Set<String>> alreadyScanned = new ConcurrentHashMap<String, Set<String>>();
	
	/*
	 * This method calls helper functions to find wiki links inside of another
	 * wiki page and returns a set of them, or null if the code runs into an
	 * error while attempting to scan the html source code. An error would mean
	 * that the code is trying to open an invalid page. An invalid link is one
	 * where the page itself says "Wikipedia does not have an article with
	 * that name" and sometimes, a page may link to something like that and
	 * redirecting doesn't completely work.
	 * 
	 * @param link: name of link to be searched
	 * 
	 * @return links, a set of link names, else null
	 * 
	 */
	public static Set<String> findWikiLinks(String link) {
		if (alreadyScanned.containsKey(link)) {
			return alreadyScanned.get(link);
		}
		// catching any invalid links
		try {
			String html = fetchHTML(link);
			Set<String> links = scrapeHTML(html);
			alreadyScanned.put(link, links);
			return links;
		} catch (Exception e) {
			// null is caught by linksInCommon() when it calls findWikiLinks()
			// to attempt to enqueue an invalid link
			return null;
		}
	}
	
	/*
	 * This function takes in a link name and opens its wiki url to go through
	 * its html code to return all of it as a String
	 * 
	 * @param link
	 * 
	 * @return a String representation of the html code of the page, or
	 * NullPointerException (or any other exception) if page doesn't exist
	 * 
	 */
	private static String fetchHTML(String link) {
		StringBuffer buffer = null;
		try {
			URL url = new URL(getURL(link));
			InputStream is = url.openStream();
			int ptr = 0;
			buffer = new StringBuffer();
			while ((ptr = is.read()) != -1) {
			    buffer.append((char)ptr);
			}
		} catch (Exception ex) {
			System.out.println(ex.getMessage());
			ex.printStackTrace();
		}
		return buffer.toString();
	}
	
	/*
	 * This method returns a wiki version url of the passed in link name
	 * 
	 * @param link
	 * 
	 */
	private static String getURL(String link) {
		return "https://en.wikipedia.org/wiki/" + link;
	}
	
	
	/*
	 * This method takes in a String representation of a link's html source
	 * code and scans it for any valid wiki links found in there. A valid link
	 * in here is defined as not having "#" or ":" in the url
	 * 
	 */
	private static Set<String> scrapeHTML(String html) {
		Set<String> wikiLinks = new HashSet<String>();
		String[] htmlSplit = html.split("<");
		for (String chars : htmlSplit) {
			if (chars.startsWith("a href=\"/wiki/")) {
				// substringing from the first occurence of / to the end 
				// to its second occurrence up to the quote in the title
				String temp = chars.substring(chars.indexOf("/") + 1); // wiki/Red"...
				String linkName = temp.substring(temp.indexOf("/") + 1,
						temp.indexOf("\"")); // Red
				
				// if neither "#" nor ":" are in the link
				if (!(linkName.contains("#")) && (!linkName.contains(":"))) {
					wikiLinks.add(linkName);
				}
			}
		}
		
		return wikiLinks;
	}
	
}
