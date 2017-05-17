<?php
define('SQLITEDBFILE','../sampleData/test.db');

////////////////////////////////////////////////////////////////////////////////
function print_pre($v,$label = "",$printme = true){
    $b = "";
    if ( $label != "" ){
        $b .= "<hr><font color=blue>$label</font>\n";
    }
    $b .= "<pre class=\"print_pre\">";

    $b .= print_r($v,true);

    $b .= "</pre>";
    if ( $label != "" ){
        $b .= "<font color=blue>$label</font><hr>\n";
    }

    if( $printme ) print $b;
    return $b;
}
////////////////////////////////////////////////////////////////////////////////
$row = array();
if( file_exists(SQLITEDBFILE)){
    $dbh = new PDO('sqlite:'. SQLITEDBFILE);
    $columns = array();
    $colinfo = $dbh->query("PRAGMA table_info('proposals')",PDO::FETCH_ASSOC);
    foreach($colinfo as $ci){
        $columns[] = $ci['name'];
    }
    //print_pre($columns,"column info");

    $dataresult = $dbh->query("SELECT * FROM proposals",PDO::FETCH_ASSOC);
    foreach($dataresult as $r){
        $row[] = $r;
        //print_pre($row,"data row direct from query");
    }
}
else {
    echo "Cant find the db file: " . SQLITEDBFILE . "<br>\n";
}

//print_pre($row,"All row data");
?>

<html>
    <head>
        <meta charset="UTF-8"/>
        <script type="text/javascript" src="//code.jquery.com/jquery-latest.js"></script>
        <script type="text/javascript" charset="utf-8" src="//cdn.datatables.net/1.10.15/js/jquery.dataTables.min.js"></script>
        <title>Raw Data</title>
        <link rel="stylesheet" type="text/css" href="//cdn.datatables.net/1.10.15/css/jquery.dataTables.min.css">
        <link rel="stylesheet" type="text/css" href="css/style.css">
    </head>

<body>
<h1>Raw Data Display using DataTables.net</h1>

<?php
// process data
//print_pre($row[0],"first row");

$iTotal=count($row);
$output = array(
    "sEcho" => 1,
    "iTotalRecords" => $iTotal,
    "iTotalDisplayRecords" => $iTotal,
    "aaData" => array()
);
// actually, not sure why we are doing this...  this should be, in essence an
// exact duplicate of the rows array (since it was read in with numerical indeces)
// + it's broken ... not sure HOW this is broken, but it is
// OH - it's expecting row data to be hashed...  thats OK, can switch that
// that way, if we nuke specific column entries from column list, then the data wont
// appear in the output :-)
//
// $row is expected to be an indexed array of rows with each row being hashed columns
for ( $j=0 ; $j<count($row) ; $j++ ){
    $aRow=array();
    for ( $i=0 ; $i<count($columns) ; $i++ ){
          $aRow[] = $row[$j][$columns[$i]];
    }
    //print_pre($aRow,"data row during conversion");
    $output['aaData'][] = $aRow;
}

//print_pre($output['aaData'],"all output data");
//$output['aaData'] = $row;

echo "<!-- data in comment\n";
$x=0;
foreach ($output['aaData'] as $value){
    if ( $x == 0) {	echo '["';	$x = 1;	}
    else {	echo ',["';	}
    echo implode('", "', $value);
    echo '"]';
}
echo "End of data in comment -->\n";
?>

    <div id="dynamic">
        <table cellpadding="0" cellspacing="0" border="0" class="display" id="table_id"></table>
    </div>

    <script>
    $(document).ready(function() {
     $('#table_id').dataTable( {
            "aaData": [
        <?php
    	$x=0;
    	foreach ($output['aaData'] as $value){
    		if ( $x == 0) {	echo '["';	$x = 1;	}
    		else {	echo ',["';	}
            echo implode('", "', $value);
            echo '"]';
    	}
    	?>
    	],
            "aoColumns": [
        <?php
            // could/should build the list below dynamically
            $titles = array();
            foreach($columns as $c) $titles[] = '{ "sTitle" : "' . $c . '"}';
            echo implode(",\n",$titles);
        ?>
                /* { "sTitle": "Seq_Num"},
                { "sTitle": "Title"},
                { "sTitle": "Agency"},
                { "sTitle": "Agency_SeqNum" },
                { "sTitle": "Agency_Number" },
                { "sTitle": "Center"  },
                { "sTitle": "Status" },
                { "sTitle": "Type" },
                { "sTitle": "Amount" },
                { "sTitle": "Start_Date" },
                { "sTitle": "End_Date" },
                { "sTitle": "OR_Record_Number" },
                { "sTitle": "Date_Submitted" },
                { "sTitle": "Fiscal_Year_Submitted"},
                { "sTitle": "Notes"},
                { "sTitle": "History"},
                { "sTitle": "IDC_Rate_Type"},
                { "sTitle": "Doc_Notes"},
                { "sTitle": "PI_Name_Display"},
                { "sTitle": "Status_Date"},
                { "sTitle": "Revised_Budget"},
                { "sTitle": "Due_Date"},
                { "sTitle": "PI_Order_Number"},
                { "sTitle": "PI_Code"},
                { "sTitle": "First_Name"},
                { "sTitle": "Last_Name"},
                { "sTitle": "Dept"},
                { "sTitle": "PI_Title"},
                { "sTitle": "epoch"}
*/
            ],
            "sScrollY": "70%",
            "bPaginate": false,
            "sScrollX": "70%",
            "sScrollXInner": "100%",
    	"bScrollCollapse": false,
    	"bAutoWidth": false

        } );
    } );
    </script>


</body>
</html>
