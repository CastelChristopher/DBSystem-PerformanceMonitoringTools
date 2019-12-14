package javaclient;

import javaclient.queries.*;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.HashMap;
import java.util.Map;

public class Main {

    private static long[] arrivals;

    private static final int NUMBER_ARRIVALS = 100;
    private static final int LAMBDA = 1;
    private static final int SELECT_LIMIT = 1000;
    private static final String BASE_PATH = "logs/java_query_";
    private static final String FILE_EXTENSION = ".log";

    private static Map<QueryType, Query> queries = new HashMap<>();

    static {
        queries.put(QueryType.SIMPLE_SELECT, new QuerySimpleSelect());
        queries.put(QueryType.ADVANCED_SELECT, new QueryAdvancedSelect());
        queries.put(QueryType.SIMPLE_INSERT, new QuerySimpleInsert());
        queries.put(QueryType.SIMPLE_UPDATE, new QuerySimpleUpdate());
        queries.put(QueryType.CLEANUP, new QueryCleanup());
    }

    public static void main(String[] args) throws InterruptedException, IOException {
        buildArrivalSimulation();
        JavaClient client = new JavaClient();

        QueryType queryType = QueryType.SIMPLE_SELECT;
        Query query = queries.get(queryType);
        String PATH = BASE_PATH + queryType + "_" + SELECT_LIMIT + "_" + System.currentTimeMillis() +  FILE_EXTENSION;
        Path path = Paths.get(PATH);
        Files.createFile(path);

        for (long arrival : arrivals) {
            Thread.sleep(arrival);
            client.executeQuery(query, path, SELECT_LIMIT);
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
