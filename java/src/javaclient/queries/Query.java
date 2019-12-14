package javaclient.queries;

import java.nio.file.Path;
import java.sql.Connection;

public interface Query {
    void execute(Connection connection, Path path, Object... params) throws Exception;
}
