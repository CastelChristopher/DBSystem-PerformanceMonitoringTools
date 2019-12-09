package javaclient.queries;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class QuerySimpleSelect implements Query {
    @Override
    public void execute(Connection connection) throws Exception {
        PreparedStatement stmt = connection.prepareStatement("SELECT * FROM employees.salaries");
        ResultSet rs = stmt.executeQuery();
    }
}
