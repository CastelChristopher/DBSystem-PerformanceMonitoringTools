package javaclient;

import org.mariadb.jdbc.MariaDbPoolDataSource;

import java.math.BigInteger;
import java.sql.Connection;
import java.sql.Date;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.SQLIntegrityConstraintViolationException;
import java.time.LocalDate;
import java.util.ArrayDeque;
import java.util.Queue;
import java.util.Random;

public class JavaClient {

    private static long[] arrivals;
    private static Random rnd = new Random();

    private static final int NUMBER_ARRIVALS = 1_000;
    private static final int LAMBDA = 1;
    private static final int QUERIES_WARMUP = 100;

    private static Queue<Tuple<Long, Date>> insertedPrimaryKeys = new ArrayDeque<>();

    public static void main(String[] args) throws InterruptedException {

        buildArrivalSimulation();

        executeQuery(1);

//        for (int i = 0; i < QUERIES_WARMUP; i++) {
//            Thread.sleep(100);
//            // executeWarmupQuery();
//        }
//
//        int queryParameter = 1;
//        for (long arrival : arrivals) {
//            for (int i = 0; i < 100; i++) {
//                Thread.sleep(arrival);
//                executeQuery(queryParameter);
//            }
//            queryParameter *= 2;
//            if (queryParameter * 2 < 2_767_313)
//                break;
//        }
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

    public static void executeQuery(int param) {
        new Thread(() -> {
            long initTime = System.nanoTime();
            try (Connection connection = DriverManager.getConnection(
                    "jdbc:mariadb://188.166.44.139:3306", "student", "1234")) {
                testSimpleInsert(connection);
//                testSimpleSelect(connection);
            } catch (SQLException e) {
                e.printStackTrace();
            }
            System.out.println(param + "," + ((System.nanoTime() - initTime) / 1e6));
        }).start();
    }

    public static void executeWarmupQuery() {
        new Thread(() -> {
            long initTime = System.nanoTime();
            try (Connection connection = DriverManager.getConnection(
                    "jdbc:mariadb://188.166.44.139:3306", "student", "1234")) {
                // TODO
                PreparedStatement stmt = connection.prepareStatement("DELETE FROM employees.salaries WHERE emp_no=0 AND from_date=''");
                ResultSet rs = stmt.executeQuery();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }).start();
    }

    public static void executeInsertsCleanup() {
        new Thread(() -> {
            long initTime = System.nanoTime();
            try (Connection connection = DriverManager.getConnection(
                    "jdbc:mariadb://188.166.44.139:3306", "student", "1234")) {
                // TODO
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }).start();
    }

    private static void testSimpleSelect(Connection connection) throws SQLException {
        PreparedStatement stmt = connection.prepareStatement("SELECT * FROM employees.salaries");
        ResultSet rs = stmt.executeQuery();
    }

    private static void testAdvancedSelect(Connection connection) throws SQLException {
        PreparedStatement stmt = connection.prepareStatement("SELECT * FROM employees.salaries S, employees.employees E WHERE S.emp_no = E.emp_no");
        ResultSet rs = stmt.executeQuery();
    }

    private static void testSimpleInsert(Connection connection) throws SQLException {
        PreparedStatement stmt = connection.prepareStatement(
                "INSERT INTO employees.salaries (emp_no, salary, from_date, to_date) VALUES(?, ?, ?, ?)",
                PreparedStatement.RETURN_GENERATED_KEYS);
        // TODO : check invalid empno
        int empNo = rnd.nextInt(1_000_000);
        stmt.setInt(1, );
        stmt.setInt(2, 12341234);
        // 100 days in milliseconds
        long from = (rnd.nextInt(90) + 10) * 100 * 3600 * 24 * 1000;
        long to = from + (rnd.nextInt(90) + 10) * 100 * 3600 * 24 * 1000;
        stmt.setDate(3, new Date(System.currentTimeMillis() - from));
        stmt.setDate(4, new Date(System.currentTimeMillis() - to));
        ResultSet rs = stmt.executeQuery();
        insertedPrimaryKeys.add(new Tuple(empNo, from));
    }

    private static void testSimpleUpdate(Connection connection) throws SQLException {
        PreparedStatement stmt = connection.prepareStatement("UPDATE employees.salaries SET salary=?, to_date=? WHERE emp_no=?");
        // TODO : check invalid empno
        int empNo = rnd.nextInt(1_000_000);
        stmt.setInt(1, 0);
        // 100 days in milliseconds
        long to = (rnd.nextInt(90) + 10) * 100 * 3600 * 24 * 1000;
        stmt.setDate(2, new Date(System.currentTimeMillis() - to));
        ResultSet rs = stmt.executeQuery();
    }

    public static class Tuple<A, B> {
        private final A a;
        private final B b;

        public Tuple(A a, B b) {
            this.a = a;
            this.b = b;
        }
    }
}
