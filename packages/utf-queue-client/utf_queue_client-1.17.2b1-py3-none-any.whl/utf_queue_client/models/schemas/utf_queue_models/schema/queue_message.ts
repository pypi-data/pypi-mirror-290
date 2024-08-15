interface QueueMessage {
    /**
     * Type of record
     */
    recordType: "UTF_TEST_EVENT" | "LOG_EVENT" | "EXCEPTION_EVENT" | "ARTIFACT_UPLOAD_REQUEST" | "OPENTELEMETRY_DATA" | "DATALAKE_DATA" | "TEST_RAIL_EVENT";
    /**
     * Subtype of record. Not all types have a subtype, but it is required when they have one.
     */
    recordSubType?: "TEST_RESULT" | "SESSION_START" | "SESSION_STOP" | "BUILD_RESULT";
    /**
     * Unique string that identifies the app/group sending the message.
     * Forward looking to match the data lake infrastructure.
     */
     tenantKey: string;
    /**
     * UTC datetime.
     * Use ISO-8601 format with time zone
     * 2022-03-10T18:50:05Z
     */
    recordTimestamp: string;

    /**
     * Record Payload.
     * This is flexible to allow different fields for different record types and DB tables
     */
    payload: QueueRecord;
}

// Older version of QueueMessage, for backwards compatibility
interface QueueMessageV1 {
    /**
     * Type of record
     */
    recordType: "UTF_TEST_EVENT" | "TEST_EVENT" | "LOG_EVENT" | "EXCEPTION_EVENT" | "ARTIFACT_UPLOAD_REQUEST";

    /**
     * Record Payload
     */
    payload: QueueRecord;

    /**
     * UTC Timestamp
     * Given in seconds since epoch (unix time)
     */
    timestamp: number;
}


interface QueueRecord {
    [key:string]: any;
}

interface DataLakeData extends QueueRecord {
    /*
    * Format of the data contained in the data field
    */ 
    dataFormat: "JSON" | "JSONSTR" | "PARQUET" | "CSV" | "NDJSON";

    /*
     * Object ID of the data payload
     * if this is not provided, a unique id will be generated
     */
    object_id?: string;
    
    /*
     * Data payload
     * if dataFormat is JSON, this is an object
     * if dataFormat is NDJSON, this is an array of objects
     * if dataFormat is JSONSTR, PARQUET or CSV, this is a base64 encoded string, with optional compression
     * as specified in the compression field
     */
    data: string | object | object[];

    /*
     * Compression format of the data field
     * if dataFormat is JSONSTR, PARQUET or CSV, this is required
     * if dataFormat is JSON or NDJSON, this is ignored
     */
    compression?: "GZIP" | "SNAPPY" | "NONE";
}

interface TelemetryData extends QueueRecord {
    dataType: "TRACES" | "LOGS" | "METRICS";
    base64ProtobufData: string;
    compression?: string;
}

interface ArtifactUploadRequest extends QueueRecord{
    name: string;
    extension: string;
    metadata: ArtifactMetadata | ArtifactBuildMetadata;
    base64Content: string;
    validateMetadata: boolean;
}

interface ArtifactMetadata {
    [key:string]: string;
}

interface ArtifactBuildMetadata {
    branch?: string;
    stack?: string;
    build_number?: string;
    target?: string;
    studio?: string;
    compiler?: string;
    app_name?: string;
    test_suite?: string;
    chip_id?: string;
    studio_build_version?: string;
    compiler_build_version?: string;
}


/**
 * Tied to the table: testdatabase.appBuildResults
 */
interface SqaAppBuildResult extends QueueRecord{

    /**
     * Logical FK to dbo.jobStatusTable.
     * Not creating the constraint in case this comes in before the session record.
     */
    session_pk_id: string;

    /**
     * Name of the application
     * @maxLength 512
     */
    app_name: string;

    /**
     * Description of what the application does
     * @maxLength 1024
     */
    app_description?: string;

    /**
     * Description of the grouping of applications
     * @maxLength 512
     */
    test_suite_name?: string;

    /**
     * Need table for validation created from the existing java enum
     * @maxLength 256
     */
    test_result_type: string;

    /**
     * Where the application was built
     * @maxLength 256
     */
    executor_name?: string;

    /**
     * Feature being tested by this test
     * @maxLength 256
     */
    feature_name?: string;

    /**
     * Description of the device type that the application runs on
     * @maxLength 256
     */
    module_name?: string;

    /**
     * Radio configuration used by the device
     * @maxLength 256
     */
    phy_name?: string;

    /**
     * Did the application build
     */
    test_result: "pass" | "fail" | "skip" | "block" | "PASS" | "FAIL";

    /**
     * Name of the engineer who created the test
     * @maxLength 256
     */
    engineer_name?: string;

    /**
     * Stack dump exception message from build
     */
    exception_msg?: string;

    /**
     * JIRA IOT Req Number
     * @maxLength 256
     */
    iot_req_id?: string;

    /**
     * Need table for validation.
     * This is the tool and version used to build the application with colon separation
     * iar:7.80.1
     * @maxLength 256
     */
    tool_chain?: string;

    /**
     * @maxLength 256
     */
    notes?: string;

    /**
     * Length of time to build the application
     */
    test_duration_sec: number;
}


/**
 * Tied to the table: testdatabase.testResults_new
 */
interface SqaTestResult extends QueueRecord {

    /**
     * Logical FK to dbo.jobStatusTable.
     * Not creating the constraint in case this comes in before the session record.
     */
    session_pk_id: string;

    /**
     * Passed in from the test executor.
     * From the test management system or git.
     * @maxLength 512
     */
    test_case_id: string;

    /**
     * @TJS-type integer
     */
    test_case_version_num: number;

    /**
     * Named group of tests
     * @maxLength 512
     */
    test_suite_name?: string;

    /**
     * What does the test case actually do
     * @maxLength 1024
     */
    test_description?: string;

    /**
     * Need to create a table for verification of this field
     * @maxLength 256
     */
    test_result_type: string
    /**
     * Test Parametric Data
     */
    test_parametric_data?: string;

    /**
     * Human readable version of the test case ID
     * Short summary/description
     * @maxLength 512
     */
    test_case_name: string;

    /**
     * Where the test actually ran
     * @maxLength 256
     */
    executor_name: string;

    /**
     * Feature being tested by this test
     * @maxLength 256
     */
    feature_name: string;

    /**
     * Date the test was created
     * ISO-8601 format
     */
    test_creation_date: string;

    /**
     * Grouping of all of the hardware used to execute the test
     * @maxLength 256
     */
    testbed_name: string; 

    /**
     * Testbed component list
     * @maxLength 256
     */
    module_name: string;

    /**
     * Radio configuration used by the device
     * @maxLength 256
     */
    phy_name?: string;

    /**
     * 
     */
    test_result: "pass" | "fail" | "skip" | "block" | "metrics";

    /**
     * Name of the engineer who created the test
     * @maxLength 256
     */
    engineer_name?: string;

    /**
     * If an error occurs, this is the message returned.
     */
    exception_msg?: string;

    /**
     * @maxLength 256
     */
    iot_req_id: string;

    /**
     * Need table for validation.
     * This is the tool and version used to build the application with colon separation
     * iar:7.80.1
     * @maxLength 256
     */
    tool_chain: string;

    /**
     * @maxLength 256
     */
    vendor_name?: string;
    
    /**
     * @maxLength 256
     */
    vendor_build?: string;
    
    /**
     * @maxLength 256
     */
    vendor_result?: string;
    
    /**
     * @maxLength 1024
     */
    notes?: string;
    
    /**
     * Change this to boolean - default false
     */
    portal_watch?: string;
    
    /**
     * Test duration in seconds
     */
    test_duration_sec: number;
    
    /**
     * @maxLength 256
     */
    test_bed_label?: string;

    /**
     * @maxLength 256
     */
    req_id?: string;

    /**
     * @maxLength 256
     */
    product_line?: string;

    /**
     * @maxLength 256
     */
    product_type?: string;

    /**
     * @maxLength 256
     */
    customer_type?: string;

    /**
     * @maxLength 1500
     */
    jenkins_test_case_results_url?: string;

    /**
     * UUID generated by the client software
     */
    test_case_uuid?: string;
}


/**
 * Tied to the table: dbo.jobStatusTable
 */
interface SqaTestSession extends QueueRecord {
    
    /**
     * UUID generated by the Jenkins client software
     */
    PK_ID: string;
    
    /**
     * ISO-8601 Datetime
     */
    startTime: string;
    
    /**
     * ISO-8601 datetime
     */
    stopTime?: string;
    
    /**
     * Status of the Jenkins job
     */
    jenkinsJobStatus: "COMPLETE" | "IN PROGRESS" | "FAIL"
    
    /**
     * Elapsed number of seconds for the Jenkins job.
     * Should be close to stop time - start time.
     * Change the data type in the DB to integer.
     * @TJS-type integer
     */
    duration?: number;
    /**
     * Type of Jenkins job
     * @maxLength 256
     */
    jobType?: string
    
    /**
     * @maxLength 256
     */
    releaseName: string;
    
    /**
     * @maxLength 256
     */
    branchName: string;
    
    /**
     * @maxLength 256
     */
    stackName: string;

    /**
     * @TJS-type integer
     */
    SDKBuildNum: number;
    
    /**
     * @maxLength 1500
     */
    SDKUrl?: string;
    
    /**
     * @maxLength 1500
     */
    studioUrl?: string;

    /**
     * @TJS-type integer
     */
    totalTests?: number;

    /**
     * @TJS-type integer
     */
    PASS_cnt?: number;

    /**
     * @TJS-type integer
     */
    FAIL_cnt?: number;

    /**
     * @TJS-type integer
     */
    SKIP_cnt?: number;

    /**
     * @TJS-type integer
     */
    BLOCK_cnt?: number;
    
    /**
     * @maxLength 256
     */
    jenkinsServerName: string;

    /**
     * @TJS-type integer
     */
    jenkinRunNum: number;
    
    /**
     * @maxLength 1500
     */
    jenkinsJobName: string;
    
    /**
     * @maxLength 1500
     */
    jenkinsTestResultsUrl: string;
    
    /**
     * @maxLength 500
     */
    traceId?: string;

    /**
     * @maxLength 256
     */
    testFramework?: string;

    /**
     * @maxLength 256
     */
    SDKVersion?: string;

    /**
     * @maxLength 256
     */
    test_run_by?: string;
}

interface LogEvent extends QueueRecord {

}

interface ExceptionEvent extends QueueRecord {

}

interface TestRailAddResult extends QueueRecord{
    id: string;

    /**
     * @TJS-type integer
     */
    run_id: number;

    status: string;

    comment?: string;

    version?: string;

    defects?: string;

    /**
     * @TJS-type integer
     */
    assigned_to_id?: number;

    custom_props?: TestResultCustomProps;
}

interface TestResultCustomProps {
    [key:string]: string;
}