package javaclient.queries;

import javaclient.Utils;

import java.nio.file.Path;
import java.sql.Connection;
import java.sql.Date;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class QuerySimpleUpdate implements Query {
    @Override
    public void execute(Connection connection, Path path, Object... params) throws Exception {
        PreparedStatement stmt = connection.prepareStatement("UPDATE employees.salaries SET salary=?, to_date=? WHERE emp_no=?");
        stmt.setInt(1, 0);
        long to = (Utils.rnd.nextInt(90) + 10) * 100 * 3600 * 24 * 1000; // 100 days in milliseconds
        stmt.setDate(2, new Date(System.currentTimeMillis() - to));
        int empNo = Utils.rnd.nextInt(1_000_000);
        stmt.setInt(3, empNo);
        try {
            ResultSet rs = stmt.executeQuery();
        } catch (Exception ignore) {}
    }
}
