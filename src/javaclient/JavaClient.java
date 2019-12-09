package javaclient;

import javaclient.queries.Query;

import java.sql.Connection;
import java.sql.DriverManager;

public class JavaClient {

    private static final String URL = "jdbc:mariadb://188.166.44.139:3306";
    private static final String USER = "student";
    private static final String PASSWORD = "1234";

    public void executeQuery(Query query) {
        new Thread(() -> {
            long initTime = System.nanoTime();
            try (Connection connection = DriverManager.getConnection(URL, USER, PASSWORD)) {
                query.execute(connection);
            } catch (Exception e) {
                e.printStackTrace();
            }
            System.out.println((System.nanoTime() - initTime) / 1e6);
        }).start();
    }

    public void executeInsertsCleanup(Query query) {
        new Thread(() -> {
            try (Connection connection = DriverManager.getConnection(URL, USER, PASSWORD)) {
                query.execute(connection);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }).start();
    }
}
