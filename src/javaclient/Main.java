package javaclient;

import javaclient.queries.*;

import java.util.HashMap;
import java.util.Map;

public class Main {

    private static long[] arrivals;

    private static final int NUMBER_ARRIVALS = 1_000;
    private static final int LAMBDA = 1;
    private static final int QUERIES_WARMUP = 100;

    private static Map<QueryType, Query> queries = new HashMap<>();

    static {
        queries.put(QueryType.SIMPLE_SELECT, new QuerySimpleSelect());
        queries.put(QueryType.ADVANCED_SELECT, new QueryAdvancedSelect());
        queries.put(QueryType.SIMPLE_INSERT, new QuerySimpleInsert());
        queries.put(QueryType.SIMPLE_UPDATE, new QuerySimpleUpdate());
        queries.put(QueryType.CLEANUP, new QueryCleanup());
    }

    public static void main(String[] args) throws InterruptedException {
        buildArrivalSimulation();
        JavaClient client = new JavaClient();

        Query query = queries.get(QueryType.SIMPLE_SELECT);
        System.out.println("WARMUP STARTED");
        for (long arrival : arrivals) {
            for (int i = 0; i < 100; i++) {
                Thread.sleep(arrival);
                client.executeQuery(query);
            }
        }
        System.out.println("WARMUP DONE");
        System.out.println("--------------------");
        for (long arrival : arrivals) {
            for (int i = 0; i < 100; i++) {
                Thread.sleep(arrival);
                client.executeQuery(query);
            }
        }
    }

    public static void buildArrivalSimulation() {
        arrivals = new long[NUMBER_ARRIVALS];
        for (int i = 0; i < NUMBER_ARRIVALS; i++) {
            arrivals[i] = (long) Math.floor((exponentialArrival(LAMBDA) * 1000)); // in milliseconds
        }
    }

    // https://stackoverflow.com/a/5615564
    public static double exponentialArrival(double lambda) {
        // https://en.wikipedia.org/wiki/Inverse_transform_sampling
        return Math.log(Math.random()) / -lambda;
    }

}
