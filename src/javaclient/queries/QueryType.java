package javaclient.queries;

public enum QueryType {
    SIMPLE_SELECT ("simple_select"),
    ADVANCED_SELECT ("advanced_select"),
    SIMPLE_INSERT ("simple_insert"),
    SIMPLE_UPDATE ("simple_update"),
    CLEANUP ("cleanup");

    String queryName;
    QueryType(String queryName) {
        this.queryName = queryName;
    }

    public String toString() {
        return queryName;
    }
}
