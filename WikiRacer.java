/*
* AUTHOR: Neha Joshi
* FILE: WikiRacer.java
* ASSIGNMENT: Programming Assignment 
* COURSE: CSc 210; Section 001; Spring 2022
* PURPOSE: This program uses input from the command line to get a start and an
* 		   end page value of valid wiki pages and returns the "fastest" possible
* 		   route between the two. Fastest can vary from run to run. It also 
* 		   prints out how long the algorithm took to find that path. It essentially
* 		   models another program called WikiRacer, where users themselves have
* 		   find the shortest route between two pages.
* 
*/

import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Set;

public class WikiRacer {
	
	public static void main(String[] args) {
		List<String> ladder = findWikiLadder(args[0], args[1]);
		System.out.println(ladder);
	}
	
	/*
	 * This method takes two wiki pages and returns a path of where to go to
	 * get to the end page and also prints how long the code took to figure that
	 * path out
	 * 
	 * @param start, end: names of the starting and ending pages
	 * 
	 * @return a list of wiki pages that lead to the end page, else an empty list
	 * if no ladder was found
	 * 
	 */
	private static List<String> findWikiLadder(String start, String end) {
		Instant begin = Instant.now(); // start the timer
		
		MaxPQ laddersQueue = new MaxPQ(end);
		try {
			laddersQueue.enqueue(new ArrayList<String>(Arrays.asList(start)));
		} catch (NoSuchElementException e) {
			System.out.println("Wikipedia does not have an article with the name " + end);
			System.exit(1); // exits the code since end page doesn't exist
		}
		
		List<String> result = wikiLadderHelper(laddersQueue, end);
		Instant finish = Instant.now(); // end the timer
		if (result.isEmpty()) {
			System.out.println("Could not find a ladder from " + start + " to " + end);
		}
		System.out.println("Time taken: " + Duration.between(begin, finish).toMillis() + " milliseconds");
		return result;
	}
	
	/*
	 * Helper function for findWikiLinks(), mainly to reduce function length
	 * 
	 * @param laddersQueue: custom-implemented binary max heap for holding ladders
	 * 
	 * @param end
	 * 
	 * @return a list/ladder of links that go from start to end, else empty list
	 * 
	 */
	private static List<String> wikiLadderHelper(MaxPQ laddersQueue, String end) {
		// when a page gets dequeued, then it's actually visited and added here
		Set<String> linksVisited = new HashSet<String>();
		
		while (!(laddersQueue.isEmpty())) {
			List<String> currLadder = laddersQueue.dequeue();
			String currPage = currLadder.get(currLadder.size() - 1); // last page is current page
			linksVisited.add(currPage);
			Set<String> currPageLinks = WikiScraper.findWikiLinks(currPage);
			
			if (currPageLinks.contains(end)) {
				currLadder.add(end);
				return currLadder;
			}
			
			currPageLinks.parallelStream().forEach(link -> {
				// scanning in the links found inside each link in the current page
				WikiScraper.findWikiLinks(link);
			});
			
			for (String link : currPageLinks) {				
				if (!(linksVisited.contains(link))) {
					List<String> copyLadder = new ArrayList<String>(currLadder);
					copyLadder.add(link);
					try {
						laddersQueue.enqueue(copyLadder);
					} catch (NoSuchElementException e) {} // the page by this name doesn't exist	
				}
			}
		}
		
		return new ArrayList<String>();
	}

}
