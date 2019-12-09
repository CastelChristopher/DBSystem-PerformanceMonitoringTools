package javaclient.queries;

import javaclient.Utils;

import java.sql.*;

public class QuerySimpleInsert implements Query {
    @Override
    public void execute(Connection connection) throws SQLException {
        PreparedStatement stmt = connection.prepareStatement(
                "INSERT INTO employees.salaries (emp_no, salary, from_date, to_date) VALUES(?, ?, ?, ?)",
                PreparedStatement.RETURN_GENERATED_KEYS);
        int empNo = Utils.rnd.nextInt(1_000_000);
        stmt.setInt(1, empNo);
        stmt.setInt(2, 12341234);
        // 100 days in milliseconds
        long from = (Utils.rnd.nextInt(90) + 10) * 100 * 3600 * 24 * 1000;
        long to = from + (Utils.rnd.nextInt(90) + 10) * 100 * 3600 * 24 * 1000;
        stmt.setDate(3, new Date(System.currentTimeMillis() - from));
        stmt.setDate(4, new Date(System.currentTimeMillis() - to));
        try {
            ResultSet rs = stmt.executeQuery();
        } catch (Exception ignore) {}
    }
}
