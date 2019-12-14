package javaclient.queries;

import java.nio.file.Path;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class QueryAdvancedSelect implements Query {
    @Override
    public void execute(Connection connection, Path path, Object... params) throws Exception {
        PreparedStatement stmt = connection.prepareStatement("SELECT * FROM employees.salaries S, employees.employees E WHERE S.emp_no = E.emp_no");
        ResultSet rs = stmt.executeQuery();
    }
}
