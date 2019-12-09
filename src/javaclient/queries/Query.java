package javaclient.queries;

import java.sql.Connection;

public interface Query {
    void execute(Connection connection) throws Exception;
}
