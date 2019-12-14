package javaclient;

import javaclient.queries.Query;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.sql.Connection;
import java.sql.DriverManager;
import java.time.Instant;

public class JavaClient {

    private static final String URL = "jdbc:mariadb://derhomeschlager.duckdns.org:3306";
    private static final String USER = "student";
    private static final String PASSWORD = "1234";

    public void executeQuery(Query query, Path path, Object... params) {
        new Thread(() -> {
            long initTime = System.nanoTime();
            try (Connection connection = DriverManager.getConnection(URL, USER, PASSWORD)) {
                query.execute(connection, path, params);
            } catch (Exception exc) {
                exc.printStackTrace();
            }
            long unixTimestamp = Instant.now().getEpochSecond();
            double queryTime =  (System.nanoTime() - initTime) / 1e6;
            try {
                Files.write(path, (unixTimestamp + " " + System.currentTimeMillis() +  " " + queryTime + "\r\n").getBytes(), StandardOpenOption.APPEND);
            } catch (IOException exc) {
                System.exit(-5);
            }
        }).start();
    }

    public void executeInsertsCleanup(Query query, Path path, Object... params) {
        new Thread(() -> {
            try (Connection connection = DriverManager.getConnection(URL, USER, PASSWORD)) {
                query.execute(connection, path, params);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }).start();
    }
}
