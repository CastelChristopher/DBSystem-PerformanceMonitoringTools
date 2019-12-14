package javaclient.queries;

import java.nio.file.Path;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class QuerySimpleSelect implements Query {
    @Override
    public void execute(Connection connection, Path path, Object... params) throws Exception {
        PreparedStatement stmt = connection.prepareStatement("SELECT * FROM employees.salaries LIMIT ?");
        stmt.setObject(1, params[0]);
        ResultSet rs = stmt.executeQuery();
    }
}
