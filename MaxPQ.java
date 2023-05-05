/*
* AUTHOR: Neha Joshi
* FILE: MaxPQ.java
* ASSIGNMENT: Programming Assignment 
* COURSE: CSc 210; Section 001; Spring 2022
* PURPOSE: This program models a max binary heap backed by an array that uses
* 		   an internal class of ladders as nodes to stores the information for
* 		   Wikipedia pages leading from the start page to the end. The priority
* 		   part is based how many links the "current page", which is the last
* 		   element in a ladder, has in common with the ending one.
* 
*/

import java.util.HashSet;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Set;

public class MaxPQ {
	// class fields
	private Set<String> END_LINKS;
	private Ladder[] binMaxHeap;
	private static final int DEFAULT_SIZE = 800;
	private int size = 0;
	
	/* Constructor */
	public MaxPQ(String end) {
		this.binMaxHeap = new Ladder[DEFAULT_SIZE];
		this.END_LINKS = WikiScraper.findWikiLinks(end);
	}
	
	/*
	 * Helper function that grows capacity of the array-backed heap as
	 * needed, by doubling it in size
	 * 
	 */
	private void growHeap() {
		Ladder[] newHeap = new Ladder[2 * binMaxHeap.length];
        System.arraycopy(binMaxHeap, 1, newHeap, 1, size);
        binMaxHeap = newHeap;
    }
	
	/*
	 * Helper function used to determine which of the two passed-in partial ladders
	 * has a higher urgency, based on the links it has in common with the end page
	 * 
	 * @param ladder1, ladder2: Ladder objects that are actually a list of wiki pages
	 * 							from the start up to the current page in the process
	 * 
	 * @return a boolean value of true if the first ladder has a higher urgency,
	 * else false
	 * 
	 */
	private boolean hasHigherUrgency(Ladder ladder1, Ladder ladder2) {
        // order always goes parent(ladder1) compared to the child(ladder2)
        // or child1 to child2
        if (ladder1.priority > ladder2.priority) {
            return true;
        } else if (ladder1.priority == ladder2.priority) {
            // if ladder1 itself is smaller than ladder2
        	// kinda arbitrary but fuck it tbh
        	return (ladder1.size() <= ladder2.size());
        }
        
        return false;
    }
	
	/*
	 * Helper function to determine the priority part of the ladder, by figuring
	 * out how many links the passed-in page has in common with the end one.
	 * Uses set intersection to figure out that number
	 * 
	 * @param currLast: name of the current page in the ladder
	 * 
	 * @return the number of links both pages have in common, else -1
	 * 
	 */
	private int linksInCommon(String currLast) {
		Set<String> copyEndLinks = new HashSet<String>(END_LINKS);
		Set<String> currPageLinks = WikiScraper.findWikiLinks(currLast);
		
		// null means the page's html can't be found
		if (currPageLinks != null) {
//			currPageLinks.retainAll(END_LINKS); // currPageLinks gets changed here
			copyEndLinks.retainAll(currPageLinks);
//			return currPageLinks.size();
			return copyEndLinks.size();
		} else {
			return -1;
		}
	}
	
	/*
	 * This method takes in a list of pages and adds it to the heap as a Ladder
	 * object
	 * 
	 * @param ladder: a list of pages in the current ladder to the end page
	 * 
	 * @return NoSuchElementException() if the ladder can't be added to the heap
	 * due to the last page not existing
	 * 
	 */
	public synchronized void enqueue(List<String> ladder) {
		// last page in the ladder is current page
		int linksInCommon = linksInCommon(ladder.get(ladder.size() - 1));
		
		if (linksInCommon == -1) {
			throw new NoSuchElementException();
		} else {
			Ladder partialLadder = new Ladder(ladder, linksInCommon);
			
			if (size >= binMaxHeap.length - 1) growHeap();
			size++;
	        binMaxHeap[size] = partialLadder; // add to the end and bubble up as needed
	        if (size > 1) bubbleUp(size);
		}
	}
	
	/*
	 * Helper function that takes in a starting position and keeps "bubbling"
	 * elements up until max binary heap order has been achieved. That means
	 * parents have a higher priority value than children. Child index element
	 * is swapped up with its parent index element until heap is balanced.
	 * 
	 * @param startPos: an integer that's the starting position of the process
	 * 
	 */
	private void bubbleUp(int startPos) {
        // initial indices
        int i = startPos;
        int parentIndex = i / 2;
        
        while (hasHigherUrgency(binMaxHeap[parentIndex], binMaxHeap[i]) == false) {
        	
            Ladder tempParent = binMaxHeap[parentIndex]; // atm towards the front
        	binMaxHeap[parentIndex] = binMaxHeap[i]; // down to up the array
            binMaxHeap[i] = tempParent; // up to down the array

            // reassign everything
            i = parentIndex;
            parentIndex = i / 2;
            if (parentIndex == 0) break; // can't bubble up any further
        }
    }
	
	/*
	 * This method takes off the highest priority element of the heap and re-sorts
	 * it to heap order by bubbling down.
	 * 
	 * @return NoSuchElementException() if queue has nothing in it, else the
	 * list part of the ladder from the highest priority element
	 * 
	 */
	public List<String> dequeue() {
        if (size == 0) {
            throw new NoSuchElementException();
        } else {
        	List<String> mostCommon = binMaxHeap[1].currSequence;
            // move the back element up to the front and reduce size
            binMaxHeap[1] = binMaxHeap[size]; binMaxHeap[size] = null;
            size--;
            if (size > 1) bubbleDown(1);
            return mostCommon;
        }
    }
	
	/*
	 * Helper function that, similar to bubbleUp(), takes in a starting position and
	 * sorts the max heap to heap order by swapping the parent with its most urgent
	 * child index element, which is determined by urgency/priority value.
	 * 
	 * @param startPos
	 * 
	 */
	private void bubbleDown(int startPos) {
        // initial indices of parent and children elements
        int i = startPos;
        int left = i * 2;
        int mostUrgentIndex;
        if (left == size) {
        	mostUrgentIndex = left;
        } else {
        	mostUrgentIndex = hasHigherUrgency(binMaxHeap[left],
            		binMaxHeap[left + 1]) ? left : left + 1;
        }
        
        // looping through until it's all sorted
        while (hasHigherUrgency(binMaxHeap[i], binMaxHeap[mostUrgentIndex]) == false) {
        	
            Ladder tempParent = binMaxHeap[i]; // atm towards the front
            binMaxHeap[i] = binMaxHeap[mostUrgentIndex]; // down to up the array
            binMaxHeap[mostUrgentIndex] = tempParent; // up to down the array

            // reassign everything
            i = mostUrgentIndex;
            left = i * 2;
            if (left == size) {
            	mostUrgentIndex = left;
            } else if (left > size) {
            	break; // if the left child is out of bounds, neither can exist
            } else {
            	mostUrgentIndex = hasHigherUrgency(binMaxHeap[left],
                		binMaxHeap[left + 1]) ? left : left + 1;
            }
        }
    }
	
	/*
	 * This function returns whether heap is empty or not
	 * 
	 * @return boolean value of true of heap size is 0, else false
	 * 
	 */
	public boolean isEmpty() {
        return (size == 0);
    }
	
	/*
	 * This function overrides the standard toString() to return a String
	 * representation of the heap in a custom manner.
	 * 
	 * @return heapToStr, a String representation of the heap
	 * 
	 */
	@Override
    public String toString() {
        String heapToStr = "{";
        
        if (size > 0) {
            for (int i = 1; i <= size; i++) {
                heapToStr += binMaxHeap[i].toString() + ", ";
            }
            // removes the final comma and space
            heapToStr = heapToStr.substring(0, heapToStr.length() - 2) + "}";

        } else {
            heapToStr += "}";
        }
        
        return heapToStr;
    }
	
	// internal ladder class to act as nodes to organize priority queue
	private class Ladder {
		// class fields
		private List<String> currSequence;
	    private int priority;
	    private int size;
	    
	    /* Constructor */
	    public Ladder(List<String> ladder, int linksInCommon) {
	        this.currSequence = ladder;
	        this.priority = linksInCommon;
	        this.size = ladder.size() - 1;
	    }
	    
	    /*
	     * Returns size of the ladder
	     * 
	     */
	    public int size() {
	    	return size;
	    }
	    
	    /*
	     * This function overrides the standard toString method and returns the
	     * list ladder and the priority, where each ladder has its priority next
	     * to it in parentheses
	     * 
	     * @return a String version of a ladder
	     * 
	     */
	    @Override
		public String toString() {
			return currSequence + " (" + priority + ")";
		}
	}
	
}
