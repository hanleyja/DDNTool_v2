'''
Created on Apr 12, 2013

@author: xmr
'''

import unittest
import time
from SFATimeSeries import SFATimeSeries

# Constants used for building the series data
#VALUE_START=1       # Starting value when adding data to the series
#VALUE_INCREMENT=1   # Amount the series value will increase for each append
#SERIES_SIZE=500     # Number of values to append to the series
#APPEND_RATE=0.01     # Time (in seconds) between calls to append()

SERIES_LENGTH=5.0   # Amount of time (in seconds) that the series should span
SERIES_SIZE=500   # Approximate number of entries in the series
                    # (This is approximate: the cutoff is actually the timespan)
SERIES_RATE=1.0     # Average rate for the series data (in units/sec).
                    # Calls to average() should return values very close to this

class SFATimeSeries_Test( unittest.TestCase):
    
    def generate_time_series(self):
        # Build up a time series that we can mess with...
        print
        print "Generating time series data.  This will take approximately %d seconds."%SERIES_LENGTH
        self._series = SFATimeSeries()
        approx_inter_item_time = SERIES_LENGTH / SERIES_SIZE
        start_time = time.time()
        append_val = 1
        self._series.append( append_val)
        while time.time() < (start_time + SERIES_LENGTH):
            last_append_time = self._series.get( self._series.size()-1)[1]
            while time.time() < (last_append_time + approx_inter_item_time):
                time.sleep( approx_inter_item_time / 100)
            
            append_val += SERIES_RATE * (time.time() - last_append_time)     
            self._series.append( append_val)
                
        print "Time series generated."

    def testAppend(self):
        SERIES_SIZE=500     # Number of values to append to the series
        START_VALUE = 10
        INCREMENT = 1
        
        local_series = SFATimeSeries(SERIES_SIZE)
        value = START_VALUE
        while local_series.size() < SERIES_SIZE:
            orig_size = local_series.size()
            local_series.append(value)
            value += INCREMENT
            self.assertEqual(orig_size+1, local_series.size(), "Append to series failed.  Series size = %d"%local_series.size())
            
        # series is now full. Verify first & last elements
        self.assertEqual(local_series.size(), SERIES_SIZE,
                          "Series was not full when it should have been.  Actual size: %d  Expected size: %d"%(local_series.size(), SERIES_SIZE))
        self.assertEqual(local_series.get(0)[0], START_VALUE, "Unexpected first value in the series.  Did we remove it during an append?")
        self.assertEqual(local_series.get(SERIES_SIZE-1)[0], value - INCREMENT,
                          "Unexpected first value in the series.  Did we remove it during an append?")
        
        
        # Add one more value and make sure the size stays at its max 
        local_series.append( value)
        value += INCREMENT
        self.assertEqual(local_series.size(), SERIES_SIZE,
                          "Unexpected series size.  Actual size: %d  Expected size: %d"%(local_series.size(), SERIES_SIZE))
        self.assertEqual(local_series.get(0)[0], START_VALUE+INCREMENT,
                         "Unexpected first value in the series.  Did we remove it during an append?")
        self.assertEqual(local_series.get(SERIES_SIZE-1)[0], value - INCREMENT,
                          "Unexpected first value in the series.  Did we remove it during an append?")
        

    def testFlush(self):
        # Note: make sure testAppend runs first because we need append() for this test
        SERIES_SIZE=50    
        local_series = SFATimeSeries()
        for i in range(SERIES_SIZE):
            local_series.append( 1)
        
        self.assertEqual(local_series.size(), SERIES_SIZE, "Expected the series to be full.  It wasn't.")
        local_series.flush()
        self.assertEqual(local_series.size(), 0, "Expected the series to be empty.  It contained %d items."%local_series.size())
                
    # verify the average() function    
    def testAverage(self):
        # Note:  Make sure this test runs *AFTER* the append and flush tests, because
        # we need both to actually work properly in order to run this test...
        
        self.generate_time_series()
        
        half_time =  SERIES_LENGTH / 2
        result = self._series.average( half_time) # use half the time series
        self.assertAlmostEqual( result[1], half_time, delta=(SERIES_LENGTH / self._series.size()),
                                msg="Actual timespan for the Average() function too far from the requested timespan." )
        
        self.assertAlmostEqual(result[0], SERIES_RATE, delta=SERIES_RATE*.005)  # accurate to 0.5%
        
    # verify the average() function works even when there's only 1 value
    def testSingleValueAverage(self):
        local_series = SFATimeSeries()
        VALUE = 25
        local_series.append( VALUE)
        result = local_series.average(100)
        self.assertEqual(VALUE, result[0],
                         "Single value average() test returned %f instead of %f"%(result[0], VALUE))
        self.assertEqual(0, result[1],
                         "Single value average() test returnd a time span of %f instead of 0"%result[1])
        
    # verify the average() function doesn't blow up when the series is empty
    #def testEmptyAverage(self):
    #    local_series = SFATimeSeries()
    #    result = local_series.average(100)
    #    
    #    self.assertEqual(VALUE, result[0],
    #                     "Single value average() test returned %f instead of %f"%(result[0], VALUE))
    #    self.assertEqual(0, result[1],
    #                     "Single value average() test returnd a time span of %f instead of 0"%result[1])
        
if __name__ == '__main__':
    unittest.main()
        
        
        