package javaclient.queries;

import java.nio.file.Path;
import java.sql.Connection;
import java.sql.PreparedStatement;

public class QueryCleanup implements Query {
    @Override
    public void execute(Connection connection, Path path, Object... params) throws Exception {
        PreparedStatement stmt = connection.prepareStatement("DELETE FROM employees.salaries WHERE salary='12341234'");
        stmt.executeQuery();
    }
}
