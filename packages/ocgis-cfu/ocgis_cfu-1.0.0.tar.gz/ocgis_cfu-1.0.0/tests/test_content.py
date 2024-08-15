test_string = """

<html lang="en"><head>
	<title>One Call Concepts Ticket List</title>
	<meta name="description" content="Locator Ticket Management">
	
        <script type="text/javascript" src="scripts/formChek.js"></script>
        <script type="text/javascript" src="scripts/clientside.js"></script>

    
        <meta charset="utf-8">
        <!-- Tell IE to not run in compatibility mode -->
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <!-- Using Pure CSS, so bring it in -->
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/pure/0.6.1/pure-min.css">
        <!-- Uses Pure CSS responsive grids, must include seperately -->
        <!--[if lte IE 8]>
            <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/pure/0.6.1/grids-responsive-old-ie-min.css">
        <![endif]-->
        <!--[if gt IE 8]><!-->
           <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/pure/0.6.1/grids-responsive-min.css">
        <!--<![endif]-->

        <!-- Our base Style sheets -->
        <link rel="stylesheet" href="/css/occ_modules/2.6.0/main/jquery-ui.min.css">

        <!-- Need a different stylesheet for IE since it doesn't understand media queries -->
        <!--[if lte IE 8]>
            <link rel="stylesheet" href="/css/occ_modules/2.6.0/main/main-old-ie.css">
        <![endif]-->
        <!--[if gt IE 8]><!-->
            <link rel="stylesheet" href="/css/occ_modules/2.12.0/main/main.css">
        <!--<![endif]-->

        <!-- Our mapping style sheet -->
        <!-- Need a different stylesheet for IE since it doesn't understand media queries -->
        <!--[if lte IE 8]>
            <link rel="stylesheet" href="/js/occ_modules/3.49.0/oimc/css/oimc-old-ie.css">
        <![endif]-->
        <!--[if gt IE 8]><!-->
            <link rel="stylesheet" href="/js/occ_modules/3.67.0/oimc/css/oimc.css">
        <!--<![endif]-->

        <!-- Bring in jQuery -->
        <!-- Can't use 2.x as it doesn't support IE8 -->
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
        <script src="//ajax.googleapis.com/ajax/libs/jqueryui/1/jquery-ui.min.js"></script>
        <!-- This is the LEAFLET library. -->
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.3.3/dist/leaflet.css">
        <script src="https://unpkg.com/leaflet@1.3.3/dist/leaflet.js"></script>

        <!-- Bring in our OCC utilities -->
        <script src="/js/occ_modules/1.14.0/utility/calendar.js"></script>
        <script src="/js/occ_modules/1.14.0/utility/infoDialogs.js"></script>
        <script src="/js/occ_modules/1.14.0/utility/loadingOverlay.js"></script>

        <!-- Needed to get IE8 working with HTML 5  -->
        <!--[if lt IE 9]>
            <script src="//cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.2/html5shiv.js"></script>
        <![endif]-->

        <script type="text/javascript">
            function popup(dest)
            {
                window.open(dest,'','toolbar=no,status=no,scrollbars=yes,location=no,menubar=no,directories=no,resizable=yes,copyhistory=no')
            }

            function popupMore(dest)
            {
                window.open(dest,'','toolbar=yes,status=no,scrollbars=yes,location=no,menubar=no,directories=no,resizable=yes,copyhistory=no')
            }
        </script>

        <!-- Needed for HTML Table sorting -->
        <script src="scripts/tablesorter.jquery.js"></script>
        <script src="scripts/tablesorter.jquery.widgets.js"></script>
        <link rel="stylesheet" href="scripts/tablesorter.default.css">

        <script type="text/javascript">
            $('table').tablesorter({
                // *** APPEARANCE ***
                // Add a theme - try 'blackice', 'blue', 'dark', 'default'
                //  'dropbox', 'green', 'grey' or 'ice'
                // to use 'bootstrap' or 'jui', you'll need to add the "uitheme"
                // widget and also set it to the same name
                // this option only adds a table class name "tablesorter-{theme}"
                theme: 'default',

                // fix the column widths
                widthFixed: false,

                // Show an indeterminate timer icon in the header when the table
                // is sorted or filtered
                showProcessing: false,

                // header layout template (HTML ok); {content} = innerHTML,
                // {icon} = <i/> (class from cssIcon)
                headerTemplate: '{content}',

                // return the modified template string
                onRenderTemplate: null, // function(index, template){ return template; },

                // called after each header cell is rendered, use index to target the column
                // customize header HTML
                onRenderHeader: function (index) {
                    // the span wrapper is added by default
                    $(this).find('div.tablesorter-header-inner').addClass('roundedCorners');
                },

                // *** FUNCTIONALITY ***
                // prevent text selection in header
                cancelSelection: true,

                // other options: "ddmmyyyy" & "yyyymmdd"
                dateFormat: "mmddyyyy",

                // The key used to select more than one column for multi-column
                // sorting.
                sortMultiSortKey: "shiftKey",

                // key used to remove sorting on a column
                sortResetKey: 'ctrlKey',

                // false for German "1.234.567,89" or French "1 234 567,89"
                usNumberFormat: true,

                // If true, parsing of all table cell data will be delayed
                // until the user initializes a sort
                delayInit: false,

                // if true, server-side sorting should be performed because
                // client-side sorting will be disabled, but the ui and events
                // will still be used.
                serverSideSorting: false,

                // *** SORT OPTIONS ***
                // These are detected by default,
                // but you can change or disable them
                // these can also be set using data-attributes or class names
                headers: {
                    // set "sorter : false" (no quotes) to disable the column
                    0: {
                        sorter: "text"
                    },
                    1: {
                        sorter: "digit"
                    },
                    2: {
                        sorter: "text"
                    },
                    3: {
                        sorter: "url"
                    }
                },

                // ignore case while sorting
                ignoreCase: true,

                // forces the user to have this/these column(s) sorted first
                sortForce: null,
                // initial sort order of the columns, example sortList: [[0,0],[1,0]],
                // [[columnIndex, sortDirection], ... ]
                sortList: [
                    [0, 0],
                    [1, 0],
                    [2, 0]
                ],

                // default sort that is added to the end of the users sort
                // selection.
                sortAppend: null,

                // starting sort direction "asc" or "desc"
                sortInitialOrder: "asc",

                // Replace equivalent character (accented characters) to allow
                // for alphanumeric sorting
                sortLocaleCompare: false,

                // third click on the header will reset column to default - unsorted
                sortReset: false,

                // restart sort to "sortInitialOrder" when clicking on previously
                // unsorted columns
                sortRestart: false,

                // sort empty cell to bottom, top, none, zero
                emptyTo: "bottom",

                // sort strings in numerical column as max, min, top, bottom, zero
                stringTo: "max",

                // extract text from the table - this is how is
                // it done by default
                textExtraction: {
                    0: function (node) {
                        return $(node).text();
                    },
                    1: function (node) {
                        return $(node).text();
                    }
                },

                // use custom text sorter
                // function(a,b){ return a.sort(b); } // basic sort
                textSorter: null,

                // *** WIDGETS ***

                // apply widgets on tablesorter initialization
                initWidgets: true,

                // include zebra and any other widgets, options:
                // 'columns', 'filter', 'stickyHeaders' & 'resizable'
                // 'uitheme' is another widget, but requires loading
                // a different skin and a jQuery UI theme.
                widgets: ['zebra', 'columns'],

                widgetOptions: {
                    // zebra widget: adding zebra striping, using content and
                    // default styles - the ui css removes the background
                    // from default even and odd class names included for this
                    // demo to allow switching themes
                    // [ "even", "odd" ]
                    zebra: [
                        "ui-widget-content even",
                        "ui-state-default odd"],

                    // uitheme widget: * Updated! in tablesorter v2.4 **
                    // Instead of the array of icon class names, this option now
                    // contains the name of the theme. Currently jQuery UI ("jui")
                    // and Bootstrap ("bootstrap") themes are supported. To modify
                    // the class names used, extend from the themes variable
                    // look for the "$.extend($.tablesorter.themes.jui" code below
                    uitheme: 'jui',

                    // columns widget: change the default column class names
                    // primary is the 1st column sorted, secondary is the 2nd, etc
                    columns: [
                        "primary",
                        "secondary",
                        "tertiary"],

                    // columns widget: If true, the class names from the columns
                    // option will also be added to the table tfoot.
                    columns_tfoot: true,

                    // columns widget: If true, the class names from the columns
                    // option will also be added to the table thead.
                    columns_thead: true,

                    // filter widget: If there are child rows in the table (rows with
                    // class name from "cssChildRow" option) and this option is true
                    // and a match is found anywhere in the child row, then it will make
                    // that row visible; default is false
                    filter_childRows: false,

                    // filter widget: If true, a filter will be added to the top of
                    // each table column.
                    filter_columnFilters: true,

                    // filter widget: css class applied to the table row containing the
                    // filters & the inputs within that row
                    filter_cssFilter: "tablesorter-filter",

                    // filter widget: Customize the filter widget by adding a select
                    // dropdown with content, custom options or custom filter functions
                    // see http://goo.gl/HQQLW for more details
                    filter_functions: null,

                    // filter widget: Set this option to true to hide the filter row
                    // initially. The rows is revealed by hovering over the filter
                    // row or giving any filter input/select focus.
                    filter_hideFilters: false,

                    // filter widget: Set this option to false to keep the searches
                    // case sensitive
                    filter_ignoreCase: true,

                    // filter widget: jQuery selector string of an element used to
                    // reset the filters.
                    filter_reset: null,

                    // Delay in milliseconds before the filter widget starts searching;
                    // This option prevents searching for every character while typing
                    // and should make searching large tables faster.
                    filter_searchDelay: 300,

                    // Set this option to true if filtering is performed on the server-side.
                    filter_serversideFiltering: false,

                    // filter widget: Set this option to true to use the filter to find
                    // text from the start of the column. So typing in "a" will find
                    // "albert" but not "frank", both have a's; default is false
                    filter_startsWith: false,

                    // filter widget: If true, ALL filter searches will only use parsed
                    // data. To only use parsed data in specific columns, set this option
                    // to false and add class name "filter-parsed" to the header
                    filter_useParsedData: false,

                    // Resizable widget: If this option is set to false, resized column
                    // widths will not be saved. Previous saved values will be restored
                    // on page reload
                    resizable: true,

                    // saveSort widget: If this option is set to false, new sorts will
                    // not be saved. Any previous saved sort will be restored on page
                    // reload.
                    saveSort: true,

                    // stickyHeaders widget: css class name applied to the sticky header
                    stickyHeaders: "tablesorter-stickyHeader"
                },

                // *** CALLBACKS ***
                // function called after tablesorter has completed initialization
                initialized: function (table) {},

                // *** CSS CLASS NAMES ***
                tableClass: 'tablesorter',
                cssAsc: "tablesorter-headerSortUp",
                cssDesc: "tablesorter-headerSortDown",
                cssHeader: "tablesorter-header",
                cssHeaderRow: "tablesorter-headerRow",
                cssIcon: "tablesorter-icon",
                cssChildRow: "tablesorter-childRow",
                cssInfoBlock: "tablesorter-infoOnly",
                cssProcessing: "tablesorter-processing",

                // *** SELECTORS ***
                // jQuery selectors used to find the header cells.
                selectorHeaders: '> thead th, > thead td',

                // jQuery selector of content within selectorHeaders
                // that is clickable to trigger a sort.
                selectorSort: "th, td",

                // rows with this class name will be removed automatically
                // before updating the table cache - used by "update",
                // "addRows" and "appendCache"
                selectorRemove: "tr.remove-me",

                // *** DEBUGING ***
                // send messages to console
                debug: false
            });

            // Extend the themes to change any of the default class names ** NEW **
            $.extend($.tablesorter.themes.jui, {
                // change default jQuery uitheme icons - find the full list of icons
                // here: http://jqueryui.com/themeroller/ (hover over them for their name)
                table: 'ui-widget ui-widget-content ui-corner-all', // table classes
                header: 'ui-widget-header ui-corner-all ui-state-default', // header classes
                icons: 'ui-icon', // icon class added to the <i> in the header
                sortNone: 'ui-icon-carat-2-n-s',
                sortAsc: 'ui-icon-carat-1-n',
                sortDesc: 'ui-icon-carat-1-s',
                active: 'ui-state-active', // applied when column is sorted
                hover: 'ui-state-hover', // hover class
                filterRow: '',
                even: 'ui-widget-content', // even row zebra striping
                odd: 'ui-state-default' // odd row zebra striping
            });
        </script>

    
        
        <style>
		@media all {
			.page-break	{ display: none; }
			html { 	background-color: #ffffff; color: #000000; }
			body { background-color: #ffffff; color: #000000; }
			table { background-color: #ffffff; color: #000000; }
			div.content { background-color: #ffffff; color: #000000; }
			div.noprint { background-color: #ffffff; color: #000000;  display: none;}
			div.heading { background-color: #ffffff; color: #000000; }
			div.pure-u-1-1 	{ background-color: #ffffff; color: #000000; }
			div.pure-u-md-1-2 { background-color: #ffffff; color: #000000; }
			div.blank-separator { background-color: #ffffff; color: #000000; }
			span.display-line-label { background-color: #ffffff; color: #000000; }
			span.display-line { background-color: #ffffff; color: #000000; }
			span.light { background-color: #ffffff; color: #000000; }
			table.transparent td, table.transparent th { background-color: #ffffff; color: #000000; }
			
			#layout { color: #000000;background-color: #ffffff; }
			#content { color: #000000;background-color: #ffffff; }
			#separator { color: #000000;background-color: #ffffff; }
			header { color: #000000;background-color: #ffffff; }
			footer { color: #000000;background-color: #ffffff; }
			.heading,h1.heading { color: #000000;background-color: #ffffff; }
			.subheading,h1.subheading,h1 { color: #000000;background-color: #ffffff; }
			.default-color { color: #000000;background-color: #ffffff; }
			.link,.link-sm { color: #000000;background-color: #ffffff; }
			.menuitem { color: #000000;background-color: #ffffff; }
			.pure-table { color: #000000;background-color: #ffffff; }
			.pure-table thead,.pure-table tr th { color: #000000;background-color: #ffffff; }
			table.transparent thead { color: #000000;background-color: #ffffff; }
			.inputs { color: #000000;background-color: #ffffff; }
		}

		@media print {
			.page-break	{ display: block; page-break-before: always; }
			
			/* Override Font Sizes for Printing */
			html { 	font-size:10px; }
			div.heading { font-size:10px; padding-top:0px;}
			/*div.pure-u-1-1 	{ font-size:10px; }*/
			/*div.pure-u-md-1-2 { font-size:10px; }*/ 
			div.pure-g [class *= "pure-u"] { font-size:10px; }
			div.blank-separator { margin: 1px; }
			span.display-line-label { font-size:10px; }
			span.display-line { font-size:10px; }
			span.light { font-size:10px; }
			table.transparent td, table.transparent th {font-size:10px;padding: 0;}
		}
		</style>
        	
  </head>
  
  <body>
    <div id="layout">
        
        <div id="content">
        
        <div class="separator noprint"></div>
 		
 		<div class="noprint">
 			<input type="button" class="button link" onclick="javascript:window.print()" value="Print"><br>
 		</div>
 		        
    
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242211946</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/08/24 13:48 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/14/24 08:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/14/24 08:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">1 DAYS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/07/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242211946&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">BUD HARTER</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">515-729-3474</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">BROADBAND INSTALLATIONS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">515-729-3474</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">603  8TH    CARROLL, IA  51401</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    budbbi@outlook.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line">BUD HARTER</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">BORING DUCT FOR FIBER AND COAX</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">MEDIACOM</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Address:</span>
                                <span class="display-line">
                                    7500
                                    
                                    NORDIC DR
                                </span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">W RIDGEWAY AVE</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">MARKING INSTRUCTIONS: MARK 20 FT EITHER SIDE OF THE POINTS IN THE ROUTE - PED TO PED. MARK FOLLOWING THE ROUTE N FOR 32 FT, THEN E 556 FT, THEN N 56 FT, THEN WSW 134 FT.
FROM THE INTERSECTION OF NORDIC DR AND W RIDGEWAY AVE, HEAD WEST ON W RIDGEWAY AVE FOR 104 FT HEAD N FOR 39 FT TO THE BEGINNING OF THE ROUTE.</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4697852, -92.4482885 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4698068, -92.4482593 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4698308, -92.4467160 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4698424, -92.4467217 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4699955, -92.4461447 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4699679, -92.4460921 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4698681, -92.4460886 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4697585, -92.4460900 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4697347, -92.4461205 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4697032, -92.4481491 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4696688, -92.4481502 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4696140, -92.4481519 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4696165, -92.4483001 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=QmQhfau%2FHF%2Bcgcl0UzWgt%2FDhLQ9OROnEst4VH%2Bq0ZqlRbgNH6a0iKteFaBox%2BEBk')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CLECIA</td>
                                                <td>WINDSTREAM ENTERPRISE</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>INS</td>
                                                <td>AUREON NETWORK SERVICES</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>W19</td>
                                                <td>IOWA DEPARTMENT OF TRANSPORTAT</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242212647</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/08/24 16:55 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/13/24 06:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/13/24 06:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">iasarahr</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">2 WEEKS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">iasarahr</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/07/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242212647&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">ALLISON HENDERSON</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-240-5880</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">ALLISON HENDERSON</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-240-5880</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">2508  HEARST RD   CEDAR FALLS, IA  50644</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> Y&nbsp;
                            <b>After 5:00:</b>Y&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    allison@hendersoncorp.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line">ALLISON HENDERSON</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">INSTALL IRRIGATION</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">ALLISON HENDERSON</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">Y</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS TWP</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">N</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Address:</span>
                                <span class="display-line">
                                    2508
                                    
                                    HEARST RD
                                </span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">UNIVERSITY AVE</span>
                                </div>
                                
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Township:</span>
                                <span class="display-line">CEDAR FALLS TWP</span>
                            </div>
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Section, Qtr Section:</span>
                                <span class="display-line">32-SE</span>
                            </div>
                            

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">MARK FROM THE WELL S TO THE N BUILDING AND FROM THE N BUILDING W 1/4 MILE AND THE N BUILDING S TO THE FIELD</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line">STAKED OF PAINTED 
PLEASE CALL </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4729892, -92.5236235 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4774877, -92.5235271 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4774890, -92.5144618 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4730155, -92.5144288 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=hruZ1DvLf8Ld0kZcImjwUvDhLQ9OROnEst4VH%2Bq0ZqkcO6LE%2BboxQ7xVo6x8DAml')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF1</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>N10</td>
                                                <td>NORTHERN NATURAL GAS COMPANY</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242212670</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/08/24 17:03 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/14/24 06:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/14/24 06:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">1 DAY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/08/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242212670&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">DUSTIN MONEYPENNY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-213-4641</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">PRICE ELECTRIC</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-213-4641</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">405  TROY RD.    ROBINS, IA  52328</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> Y&nbsp;
                            <b>After 5:00:</b>Y&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    Dmoneypenny@priceelectric.us
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">INSTALLING FIBER</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">CITY OF WATERLOO FIBER</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">Y</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">MOUNT VERNON TWP</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">N</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Work is on or along:</span>
                                <span class="display-line">W DUNKERTON RD</span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">WAGNER RD</span>
                                </div>
                                
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Township:</span>
                                <span class="display-line">MOUNT VERNON TWP</span>
                            </div>
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Section, Qtr Section:</span>
                                <span class="display-line">28-SE</span>
                            </div>
                            

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">MARKING INSTRUCTIONS: MARK 35 FT EITHER SIDE OF THE ROUTE MARKED IN WHITE PAINT. MARK FOLLOWING THE ROUTE E FOR 1895 FT.
FROM THE INTERSECTION OF W DUNKERTON RD AND WAGNER RD, HEAD WEST ON W DUNKERTON RD FOR 0.184 MI HEAD N FOR 55 FT TO THE BEGINNING OF THE ROUTE.</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line">ADDITIONAL TSQ: MOUNT VERNON TWP S-27SW,MOUNT VERNON TWP S-33NE,MOUNT VERNON TWP S-34NW </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5708100, -92.3789468 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5708336, -92.3780980 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5708416, -92.3772161 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5708111, -92.3747507 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5708089, -92.3735978 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5708086, -92.3734678 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5706165, -92.3734685 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5706189, -92.3747533 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5706494, -92.3772167 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5706416, -92.3780916 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5706178, -92.3789459 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5706178, -92.3789461 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5706574, -92.3806457 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5706604, -92.3807756 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5708524, -92.3807674 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=079BGL6LZ47Arx1Z993H3fDhLQ9OROnEst4VH%2Bq0ZqnQ0dX5bhJBG7aV9aW94UmT')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF8</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>M58E</td>
                                                <td>MIDAMER-ELEC</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>M58G</td>
                                                <td>MIDAMER-GAS</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>WWW</td>
                                                <td>WATERLOO WATER WORKS</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242220151</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/09/24 07:34 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/14/24 08:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/14/24 08:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">1 DAY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/08/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242220151&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">JUSTIN PETERSEN</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-231-5583</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">HUDSON HARDWARE</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-231-5583</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">520  MAIN ST, PO BOX 90    HUDSON, IA  50643</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> Y&nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    HHPHOFFICE@PETERSENHHPH.COM
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line">3192315583</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-988-3231</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">TILE LINE INSTALL</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">CITY OF CEDAR FALLS</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Work is on or along:</span>
                                <span class="display-line">MCCLAIN DR</span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">PRIMROSE DR</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">PLEASE LOCATE AREA MARKED ON THE MAP. PLEASE PAINT AND FLAG.</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5043875, -92.4260427 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5043885, -92.4259126 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5040405, -92.4259100 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5040415, -92.4260414 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=A5yaUig%2FrSV9jt9Z9HQtFfDhLQ9OROnEst4VH%2Bq0ZqnZbDShEXNycPG%2Fuox2PwKL')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Marked</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242220260</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/09/24 08:23 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/14/24 07:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/14/24 07:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">30 DAY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/08/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242220260&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">DENISE MURPHY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-226-6000</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">MATTHIAS LANDSCAPING</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-226-6000</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">3170  WAGNER    WATERLOO, IA  50703</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> Y&nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    denise@matthiaslandscaping.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line">DOUG</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-230-5336</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">INSTALLING LANDSCAING</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">RAVI</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">UNION TWP</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">N</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Address:</span>
                                <span class="display-line">
                                    8024
                                    
                                    SLAP TAIL TRL
                                </span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">BEAVER RIDGE CIR</span>
                                </div>
                                
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Township:</span>
                                <span class="display-line">UNION TWP</span>
                            </div>
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Section, Qtr Section:</span>
                                <span class="display-line">32-NE</span>
                            </div>
                            

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">MARKING INSTRUCTIONS: MARK WEST SIDE OF THE DRIVEWAY IN FRONT YARD.</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5667340, -92.5172555 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5661416, -92.5162153 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5663153, -92.5155001 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5663831, -92.5155234 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5671016, -92.5158132 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=DiKEfMjDjexW4%2F2oo4sUjfDhLQ9OROnEst4VH%2Bq0ZqloYrMWQnRrwfWiaLC3Flyg')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF1</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CIW3</td>
                                                <td>IOWA REGIONAL UTILITY ASSOC</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>PN3</td>
                                                <td>BLACK HILLS ENERGY GRIMES</td>
                                        
                                                <td>Marked</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242220460</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/09/24 09:20 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/14/24 06:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/14/24 06:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">2 WEEKS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/08/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242220460&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">BAKER ENTERPRISES INC</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-352-2193</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">BAKER ENTERPRISES INC</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-352-2193</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">2203 EAST BREME  E. BREMER    WAVERLY, IA  50677</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    joshua.kullen@baker-companies.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">SITE EXCAVATION AND UTILITIES</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">BAKER ENTERPRISES INC</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Address:</span>
                                <span class="display-line">
                                    4421
                                    
                                    HUDSON RD
                                </span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">GREENHILL RD</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">MARKING INSTRUCTIONS: MARK ENTIRE PROPERTY.</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4985946, -92.4695160 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4974882, -92.4695163 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4975020, -92.4654390 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4985999, -92.4654390 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4986025, -92.4656970 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=Aa3lzafVSoGZuEHIvQ7SoPDhLQ9OROnEst4VH%2Bq0ZqlsE%2B8TBU4xY3cFTk6n6bWO')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Marked</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Marked</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>INS</td>
                                                <td>AUREON NETWORK SERVICES</td>
                                        
                                                <td>Marked</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242220551</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/09/24 09:42 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/14/24 10:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/14/24 10:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">3 DAYS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/08/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242220551&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">MATT WELLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-404-9133</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">WELLS HOLLOW LANDSCAPING</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-404-9133</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">3308  BREMER    WAVERLY, IA  50677</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> Y&nbsp;
                            <b>After 5:00:</b>Y&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    wellshollow@gmail.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line">JACK BLOMQUIST</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-483-8857</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">LANDSCAPE</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">HURST</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">Y</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">GRUNDY</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">FAIRFIELD TWP</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">N</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Address:</span>
                                <span class="display-line">
                                    32944
                                    
                                    110TH STREET
                                </span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">X AVE</span>
                                </div>
                                
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Township:</span>
                                <span class="display-line">FAIRFIELD TWP</span>
                            </div>
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Section, Qtr Section:</span>
                                <span class="display-line">11-NE</span>
                            </div>
                            

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">PLEASE MARK OUT AROUND THE ENTIRE HOUSE.</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5416227, -92.5757600 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5416732, -92.5758076 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5416919, -92.5757057 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5417305, -92.5757044 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5417601, -92.5757285 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5417680, -92.5756802 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5418085, -92.5757070 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5418006, -92.5757446 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5418402, -92.5757620 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5418085, -92.5758854 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5417492, -92.5758653 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5417384, -92.5759216 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5416514, -92.5758854 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5416415, -92.5759149 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5415368, -92.5758559 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5415269, -92.5759230 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5415506, -92.5759686 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5416909, -92.5760249 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5417700, -92.5760262 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5418569, -92.5760329 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5419202, -92.5759887 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5419380, -92.5759230 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5419498, -92.5758492 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5419587, -92.5757902 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5419597, -92.5756923 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5419410, -92.5756520 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5419192, -92.5756118 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5418736, -92.5755763 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5417620, -92.5754878 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5416593, -92.5754489 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5416395, -92.5755065 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5416227, -92.5755789 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5416217, -92.5756675 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=LGEw5miBQkHKJtuvXxBgn%2FDhLQ9OROnEst4VH%2Bq0ZqkeLI%2FdfiLhRIzrHFxrFY0%2B')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF1</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242220646</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/09/24 10:15 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/14/24 06:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/14/24 06:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">3 MONTHS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/08/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242220646&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">BRADY BOWN</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-345-2713</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">PETERSON CONTRACTORS INC.</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-345-2713</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">104  BLACKHAWK    REINBECK, IA  50669</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line">000-000-0000</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> &nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    bbown@petersoncontractors.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line">BRADY BOWN</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-415-6715</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">STREET RECONSTRUCTION</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">PETERSON CONTRACTORS INC.</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">Y</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Work is on or along:</span>
                                <span class="display-line">W RIDGEWAY AVE</span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">STATE HWY 58</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">THIS TICKET CONTAINS 2 ROUTES. 

MARKING INSTRUCTIONS: THE FIRST ROUTE IS LOCATED 559 FT E FROM THE INTERSECTION OF W RIDGEWAY AVE AND STATE HWY 58. MARK 50 FT EITHER SIDE OF THE POINTS IN THE ROUTE - RIDGEWAY. MARK FOLLOWING THE ROUTE W FOR 1154 FT.
FROM THE INTERSECTION OF W RIDGEWAY AVE AND STATE HWY 58, HEAD WEST ON W RIDGEWAY AVE FOR 0.202 MI.  AT THE TRAFFIC CIRCLE, TAKE THE 4TH EXIT AND STAY ON W RIDGEWAY AVE FOR 0.474 MI.  MAKE A U-TURN AT ACE PL FOR 0.111 MI HEAD N FOR 7 FT TO THE BEGINNING OF THE ROUTE.

MARKING INSTRUCTIONS: THE SECOND ROUTE IS LOCATED 69 FT N FROM THE INTERSECTION OF NORDIC DR AND W RIDGEWAY AVE. MARK 50 FT EITHER SIDE OF THE POINTS IN THE ROUTE - NORDIC. MARK FOLLOWING THE ROUTE N FOR 103 FT.
FROM THE INTERSECTION OF NORDIC DR AND W RIDGEWAY AVE, HEAD NORTH ON NORDIC DR FOR 59 FT HEAD E FOR 3 FT TO THE BEGINNING OF THE ROUTE.</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line">RELOCATE: CUSTOMER IS NOT REQUESTING ANY UTILITIES REMARK THEIR FACILITIES FOR THIS RELOCATE.  RELOCATE REASON: AREA TO BE MARKED WITH PAINT AND FLAGS ATTACHMENTS: NO </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4694464, -92.4479981 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4694470, -92.4481835 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4697215, -92.4481817 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4697053, -92.4437131 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4697047, -92.4435277 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4694302, -92.4435295 )
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 2:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4700118, -92.4479837 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4701487, -92.4479720 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4701314, -92.4476020 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4697127, -92.4476378 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695758, -92.4476495 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695931, -92.4480195 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=muYA%2Fn0iVnVezEleC8%2Fd7PDhLQ9OROnEst4VH%2Bq0Zqm5zKmiCmfHVuqh48rmhtrA')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CLECIA</td>
                                                <td>WINDSTREAM ENTERPRISE</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>INS</td>
                                                <td>AUREON NETWORK SERVICES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>W19</td>
                                                <td>IOWA DEPARTMENT OF TRANSPORTAT</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242220687</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/09/24 10:21 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/14/24 06:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/14/24 06:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">1 DAYS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/08/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242220687&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">MIKE ASCHER</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-268-5374</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">CEDAR FALLS UTILITIES</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-268-5374</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">1  UTILITY    CEDAR FALLS, IA  50613</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> Y&nbsp;
                            <b>After 5:00:</b>Y&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    michael.ascher@cfunet.net
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line">PAT GIESLER</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-404-9785</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">REPLACE GAS VALVES</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">CFU</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">Y</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Work is on or along:</span>
                                <span class="display-line">MAIN ST</span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">W 15TH ST</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">THIS TICKET CONTAINS 4 CIRCLES. 

MARKING INSTRUCTIONS: THE CENTER OF THE FIRST CIRCLE IS LOCATED 39 FT NE FROM THE INTERSECTION OF MAIN ST AND W 15TH ST. MARK A 10 FT RADIUS AROUND THE VALVE - GAS VALVE NORTHEAST CORNER OF INTERSECTION..
FROM THE INTERSECTION OF MAIN ST AND W 15TH ST, HEAD EAST ON E 15TH ST FOR 22 FT HEAD N FOR 30 FT TO THE VALVE.

MARKING INSTRUCTIONS: THE CENTER OF THE SECOND CIRCLE IS LOCATED 42 FT SE FROM THE INTERSECTION OF E 15TH ST AND MAIN ST. MARK A 10 FT RADIUS AROUND THE VALVE - GAS VALVE SOUTHEAST CORNER OF INTERSECTION..
FROM THE INTERSECTION OF E 15TH ST AND MAIN ST, HEAD EAST ON E 15TH ST FOR 36 FT HEAD S FOR 26 FT TO THE VALVE.

MARKING INSTRUCTIONS: THE CENTER OF THE THIRD CIRCLE IS LOCATED 43 FT SSE FROM THE INTERSECTION OF MAIN ST AND W 15TH ST. MARK A 10 FT RADIUS AROUND THE VALVE - GAS VALVE SOUTHEAST CORNER OF INTERSECTION..
FROM THE INTERSECTION OF MAIN ST AND W 15TH ST, HEAD EAST ON E 15TH ST FOR 19 FT HEAD S FOR 41 FT TO THE VALVE.

MARKING INSTRUCTIONS: THE CENTER OF THE FOURTH CIRCLE IS LOCATED 63 FT WSW FROM THE INTERSECTION OF W 15TH ST AND MAIN ST. MARK A 10 FT RADIUS AROUND THE VALVE - GAS VALVE SOUTHWEST CORNER OF INTERSECTION..
FROM THE INTERSECTION OF W 15TH ST AND MAIN ST, HEAD WEST ON E 15TH ST FOR 59 FT HEAD S FOR 26 FT TO THE VALVE.</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249996, -92.4453359 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249925, -92.4453378 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249857, -92.4453410 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249793, -92.4453453 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249734, -92.4453507 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249680, -92.4453571 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249633, -92.4453644 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249593, -92.4453724 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249561, -92.4453812 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249538, -92.4453904 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249524, -92.4453999 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249519, -92.4454096 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249524, -92.4454193 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249538, -92.4454288 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249561, -92.4454380 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249593, -92.4454468 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249633, -92.4454548 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249680, -92.4454621 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249734, -92.4454685 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249793, -92.4454739 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249857, -92.4454782 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249925, -92.4454814 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249996, -92.4454833 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250067, -92.4454839 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250138, -92.4454833 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250209, -92.4454814 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250277, -92.4454782 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250341, -92.4454739 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250400, -92.4454685 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250454, -92.4454621 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250501, -92.4454548 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250541, -92.4454468 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250573, -92.4454380 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250596, -92.4454288 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250610, -92.4454193 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250615, -92.4454096 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250610, -92.4453999 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250596, -92.4453904 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250573, -92.4453812 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250541, -92.4453724 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250501, -92.4453644 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250454, -92.4453571 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250400, -92.4453507 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250341, -92.4453453 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250277, -92.4453410 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250209, -92.4453378 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250138, -92.4453359 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5250067, -92.4453353 )
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 2:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248464, -92.4452930 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248393, -92.4452949 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248325, -92.4452981 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248261, -92.4453024 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248202, -92.4453078 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248148, -92.4453142 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248101, -92.4453215 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248061, -92.4453295 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248029, -92.4453383 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248006, -92.4453475 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247992, -92.4453570 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247987, -92.4453667 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247992, -92.4453764 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248006, -92.4453859 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248029, -92.4453951 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248061, -92.4454039 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248101, -92.4454119 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248148, -92.4454192 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248202, -92.4454256 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248261, -92.4454310 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248325, -92.4454353 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248393, -92.4454385 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248464, -92.4454404 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248535, -92.4454410 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248606, -92.4454404 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248677, -92.4454385 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248745, -92.4454353 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248809, -92.4454310 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248868, -92.4454256 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248922, -92.4454192 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248969, -92.4454119 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249009, -92.4454039 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249041, -92.4453951 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249064, -92.4453859 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249078, -92.4453764 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249083, -92.4453667 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249078, -92.4453570 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249064, -92.4453475 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249041, -92.4453383 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249009, -92.4453295 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248969, -92.4453215 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248922, -92.4453142 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248868, -92.4453078 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248809, -92.4453024 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248745, -92.4452981 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248677, -92.4452949 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248606, -92.4452930 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248535, -92.4452924 )
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 3:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248059, -92.4453547 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247988, -92.4453566 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247920, -92.4453598 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247856, -92.4453641 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247797, -92.4453695 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247743, -92.4453759 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247696, -92.4453832 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247656, -92.4453912 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247624, -92.4454000 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247601, -92.4454092 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247587, -92.4454187 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247582, -92.4454284 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247587, -92.4454381 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247601, -92.4454476 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247624, -92.4454568 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247656, -92.4454656 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247696, -92.4454736 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247743, -92.4454809 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247797, -92.4454873 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247856, -92.4454927 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247920, -92.4454970 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247988, -92.4455002 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248059, -92.4455021 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248130, -92.4455027 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248201, -92.4455021 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248272, -92.4455002 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248340, -92.4454970 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248404, -92.4454927 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248463, -92.4454873 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248517, -92.4454809 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248564, -92.4454736 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248604, -92.4454656 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248636, -92.4454568 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248659, -92.4454476 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248673, -92.4454381 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248678, -92.4454284 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248673, -92.4454187 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248659, -92.4454092 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248636, -92.4454000 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248604, -92.4453912 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248564, -92.4453832 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248517, -92.4453759 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248463, -92.4453695 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248404, -92.4453641 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248340, -92.4453598 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248272, -92.4453566 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248201, -92.4453547 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248130, -92.4453541 )
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 4:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248445, -92.4456350 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248374, -92.4456369 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248306, -92.4456401 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248242, -92.4456444 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248183, -92.4456498 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248129, -92.4456562 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248082, -92.4456635 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248042, -92.4456715 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248010, -92.4456803 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247987, -92.4456895 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247973, -92.4456990 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247968, -92.4457087 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247973, -92.4457184 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5247987, -92.4457279 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248010, -92.4457371 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248042, -92.4457459 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248082, -92.4457539 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248129, -92.4457612 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248183, -92.4457676 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248242, -92.4457730 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248306, -92.4457773 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248374, -92.4457805 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248445, -92.4457824 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248516, -92.4457830 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248587, -92.4457824 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248658, -92.4457805 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248726, -92.4457773 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248790, -92.4457730 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248849, -92.4457676 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248903, -92.4457612 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248950, -92.4457539 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248990, -92.4457459 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249022, -92.4457371 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249045, -92.4457279 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249059, -92.4457184 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249064, -92.4457087 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249059, -92.4456990 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249045, -92.4456895 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249022, -92.4456803 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248990, -92.4456715 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248950, -92.4456635 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248903, -92.4456562 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248849, -92.4456498 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248790, -92.4456444 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248726, -92.4456401 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248658, -92.4456369 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248587, -92.4456350 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5248516, -92.4456344 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=KNK3SD1ov%2FDTieQvLWt%2F0fDhLQ9OROnEst4VH%2Bq0ZqkNs4z10mdaBWoBD4nfE3s4')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CLECIA</td>
                                                <td>WINDSTREAM ENTERPRISE</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242221083</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/09/24 12:28 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/14/24 06:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/14/24 06:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">1 DAY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/08/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242221083&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">SKYLA</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-270-3784</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">BROADBAND</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-270-3784</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">5907  PO BOX 728    CARROLL, IA  51401</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    skylabbi@outlook.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line">SKYLA</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-270-3784</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">INSTALLING CATV SERVICE</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">MEDIACOM</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">Y</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Address:</span>
                                <span class="display-line">
                                    2235
                                    
                                    LINCOLN ST
                                </span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">W AIRLINE HWY</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">MARKING INSTRUCTIONS: MARK TRAILER 84 FROM THE MEDIACOM PED/POLE TO THE ELECTRICAL METER ON THE HOUSE.</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5408408, -92.4165321 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5391471, -92.4164946 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5391517, -92.4175985 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5408494, -92.4176453 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5408459, -92.4172000 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5408130, -92.4171993 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5408087, -92.4166427 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5408416, -92.4166434 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=TFjS25VEnSGev2P7vtaZLvDhLQ9OROnEst4VH%2Bq0ZqmkDWdDHjYul7Avpx%2BTSCjz')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>M58E</td>
                                                <td>MIDAMER-ELEC</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>M58G</td>
                                                <td>MIDAMER-GAS</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>WWM</td>
                                                <td>WATERLOO WMSD</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>WWW</td>
                                                <td>WATERLOO WATER WORKS</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242221084</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/09/24 12:28 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/14/24 06:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/14/24 06:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">1 DAY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/08/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242221084&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">SKYLA</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-270-3784</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">BROADBAND</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-270-3784</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">5907  PO BOX 728    CARROLL, IA  51401</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    skylabbi@outlook.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line">SKYLA</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-270-3784</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">INSTALLING CATV SERVICE</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">MEDIACOM</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">Y</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">WATERLOO</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Address:</span>
                                <span class="display-line">
                                    2235
                                    
                                    LINCOLN ST
                                </span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">W AIRLINE HWY</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">THIS TICKET CONTAINS 2 PROPERTIES. 

MARKING INSTRUCTIONS: MARK TRAILER 84 FROM THE MEDIACOM PED/POLE TO THE ELECTRICAL METER ON THE HOUSE.

MARKING INSTRUCTIONS: MARK TRAILER 84 FROM THE MEDIACOM PED/POLE TO THE ELECTRICAL METER ON THE HOUSE.</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5401973, -92.4155537 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5401342, -92.4155523 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5401360, -92.4150902 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5383169, -92.4150297 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5383145, -92.4164762 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5414319, -92.4165452 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5414355, -92.4155811 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5411176, -92.4155741 )
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 2:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5408408, -92.4165321 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5391471, -92.4164946 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5391517, -92.4175985 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5408494, -92.4176453 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5408459, -92.4172000 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5408130, -92.4171993 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5408087, -92.4166427 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5408416, -92.4166434 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=6xV5sfFxViA3j%2FF2%2BG5QCfDhLQ9OROnEst4VH%2Bq0Zql9i%2FCGMkSn5OTSo%2FgR2bUd')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CLECIA</td>
                                                <td>WINDSTREAM ENTERPRISE</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>FM8</td>
                                                <td>FARMERS MUTUAL TELEPHONE</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>M58E</td>
                                                <td>MIDAMER-ELEC</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>M58G</td>
                                                <td>MIDAMER-GAS</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>WWM</td>
                                                <td>WATERLOO WMSD</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>WWW</td>
                                                <td>WATERLOO WATER WORKS</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242221299</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/09/24 13:10 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/14/24 08:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/14/24 08:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">2 DAYS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/08/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242221299&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">DAVE HOFFMAN</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-269-3322</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">HOFFMAN &amp; HOFFMAN TRENCHING</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-269-3322</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">3822  AIRLINE HWY  PO BOX 866    CEDAR FALLS, IA  50613</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line">319-232-2453</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> &nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>Y&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    hoffmantrenching@gmail.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line">NICK HOFFMAN</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-269-3321</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">SERVICE</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">CFU</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">Y</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Work is on or along:</span>
                                <span class="display-line">WILD HORSE DR</span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">BLAIR RDG</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">MARKING INSTRUCTIONS: MARK 10 FT EITHER SIDE OF THE FLAGGED ROUTE. MARK FOLLOWING THE ROUTE ESE FOR 131 FT.
FROM THE INTERSECTION OF WILD HORSE DR AND BLAIR RDG, HEAD NORTH ON WILD HORSE DR FOR 0.141 MI.  TURN RIGHT ONTO SONOMA DR FOR 426 FT HEAD SE FOR 19 FT TO THE BEGINNING OF THE ROUTE.</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5242918, -92.5004415 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5242855, -92.5004054 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5242320, -92.5004226 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5243214, -92.5009307 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5243277, -92.5009668 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5243812, -92.5009496 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=g3RujS80jxluB6YFLEOD0PDhLQ9OROnEst4VH%2Bq0ZqmYlohoEMRKu9L4yVFCyDgM')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242221311</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/09/24 13:13 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/14/24 08:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/14/24 08:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">2 DAYS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/08/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242221311&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">DAVE HOFFMAN</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-269-3322</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">HOFFMAN &amp; HOFFMAN TRENCHING</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-269-3322</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">3822  AIRLINE HWY  PO BOX 866    CEDAR FALLS, IA  50613</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line">319-232-2453</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> &nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>Y&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    hoffmantrenching@gmail.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line">NICK HOFFMAN</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-269-3321</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">SERVICE</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">CFU</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">Y</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Address:</span>
                                <span class="display-line">
                                    4420
                                    
                                    GRANITE RIDGE RD
                                </span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">ROCKY RIDGE RD</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">MARKING INSTRUCTIONS: MARK 10 FT EITHER SIDE OF THE FLAGGED ROUTE. MARK FOLLOWING THE ROUTE NNW FOR 48 FT.
FROM THE INTERSECTION OF GRANITE RIDGE RD AND ROCKY RIDGE RD, HEAD WEST ON GRANITE RIDGE RD FOR 0.167 MI HEAD NNW FOR 93 FT TO THE BEGINNING OF THE ROUTE.</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5244352, -92.4996515 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5244611, -92.4996638 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5244793, -92.4995938 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5243289, -92.4995225 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5243030, -92.4995102 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5242848, -92.4995802 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=h5zWYhetsS9nGbJShLSToPDhLQ9OROnEst4VH%2Bq0ZqmxxADEHoBC3TfMHGEyPrz2')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242221327</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/09/24 13:17 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/14/24 08:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/14/24 08:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">2 DAYS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/08/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242221327&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">DAVE HOFFMAN</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-269-3322</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">HOFFMAN &amp; HOFFMAN TRENCHING</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-269-3322</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">3822  AIRLINE HWY  PO BOX 866    CEDAR FALLS, IA  50613</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line">319-232-2453</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> &nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>Y&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    hoffmantrenching@gmail.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line">NICK HOFFMAN</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-269-3321</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">SERVICE</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">CFU</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">Y</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Address:</span>
                                <span class="display-line">
                                    4637
                                    
                                    WILD HORSE DR
                                </span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">BLAIR RDG</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">MARKING INSTRUCTIONS: MARK 10 FT EITHER SIDE OF THE FLAGGED ROUTE. MARK FOLLOWING THE ROUTE SSW FOR 103 FT.
FROM THE INTERSECTION OF WILD HORSE DR AND BLAIR RDG, HEAD NORTH ON WILD HORSE DR FOR 0.207 MI HEAD SW FOR 49 FT TO THE BEGINNING OF THE ROUTE.</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5238234, -92.5028719 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5237976, -92.5028844 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5238162, -92.5029543 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5241069, -92.5028129 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5241327, -92.5028004 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5241141, -92.5027305 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=BCH2igfFTIK2VLuD6Or9ZPDhLQ9OROnEst4VH%2Bq0Zqn%2BTcPMhL7DO%2BKHWrmHqO3d')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242221335</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/09/24 13:19 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/14/24 08:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/14/24 08:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">2 DAYS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/08/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242221335&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">DAVE HOFFMAN</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-269-3322</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">HOFFMAN &amp; HOFFMAN TRENCHING</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-269-3322</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">3822  AIRLINE HWY  PO BOX 866    CEDAR FALLS, IA  50613</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line">319-232-2453</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> &nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>Y&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    hoffmantrenching@gmail.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line">NICK HOFFMAN</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-269-3321</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">ELECTRIC</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">CFU</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">Y</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Address:</span>
                                <span class="display-line">
                                    2604
                                    
                                    HIAWATHA RD
                                </span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">WESTERN AVE</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">MARKING INSTRUCTIONS: MARK 10 FT EITHER SIDE OF THE FLAGGED ROUTE. MARK FOLLOWING THE ROUTE S FOR 121 FT, THEN E 72 FT.
FROM THE INTERSECTION OF HIAWATHA RD AND WESTERN AVE, HEAD NORTH ON HIAWATHA RD FOR 400 FT HEAD W FOR 31 FT TO THE BEGINNING OF THE ROUTE.</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5591915, -92.4626630 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5591915, -92.4624317 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5591915, -92.4623946 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5591367, -92.4623946 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5591390, -92.4627184 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5591503, -92.4627337 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5594959, -92.4627397 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5595234, -92.4627400 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5595237, -92.4626657 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=N86gSoeEQKQHrE9fhxZSRfDhLQ9OROnEst4VH%2Bq0ZqmtJ5BCG1Gl2Ipe6MXaNv0w')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242221485</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/09/24 13:53 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/14/24 08:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/14/24 08:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">1 DAY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">iarachel</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/08/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242221485&amp;revNumber=1&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">DALE NIEMAN</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">262-893-8403</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">FNR EXCAVATION LLC</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">262-893-8403</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">32587  UTICA    NEW HARTFORD, IA  50660</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    dnieman64@gmail.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">SOIL TESTING</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">STEVE BURRELL</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Work is on or along:</span>
                                <span class="display-line">DUNKERTON RD</span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">MAVERICK AVE</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">THIS TICKET CONTAINS 3 PROPERTIES. 

MARKING INSTRUCTIONS: THE FIRST PARCEL IS LOCATED 296 FT SW FROM THE INTERSECTION OF DUNKERTON RD AND MAVERICK AVE. MARK ENTIRE PROPERTY.
FROM THE INTERSECTION OF DUNKERTON RD AND MAVERICK AVE, HEAD WEST ON DUNKERTON RD FOR 246 FT TO THE SITE ON THE S SIDE OF THE STREET.

MARKING INSTRUCTIONS: THE SECOND PROPERTY IS 411 E DUNKERTON RD. MARK ENTIRE PROPERTY.
FROM THE INTERSECTION OF DUNKERTON RD AND MAVERICK AVE, HEAD WEST ON DUNKERTON RD FOR 13 FT.  TURN LEFT AT THE 1ST CROSS STREET ONTO MAVERICK AVE FOR 164 FT TO THE SITE ON THE W SIDE OF THE STREET.

MARKING INSTRUCTIONS: THE THIRD PARCEL IS LOCATED 181 FT SSW FROM THE INTERSECTION OF MAVERICK AVE AND DUNKERTON RD. MARK ENTIRE PROPERTY.
FROM THE INTERSECTION OF MAVERICK AVE AND DUNKERTON RD, HEAD WEST ON DUNKERTON RD FOR 13 FT.  TURN LEFT AT THE 1ST CROSS STREET ONTO MAVERICK AVE FOR 164 FT TO THE SITE ON THE W SIDE OF THE STREET.</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line">NEED TO MARK EVERYTHING BEHIND THE HOUSE AND POSSIBLY EAST OF THE HOUSE.  A NEW SEPTIC MUST BE INSTALLED. </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5695483, -92.4422326 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5695485, -92.4425388 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5701357, -92.4425352 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5701355, -92.4422291 )
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 2:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5695481, -92.4418820 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5695483, -92.4422326 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5701355, -92.4422291 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5701353, -92.4418788 )
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 3:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5695479, -92.4416203 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5695481, -92.4418820 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5701353, -92.4418788 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5701351, -92.4416170 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=VxednQz1cRsy%2F3OfjFbo6%2FDhLQ9OROnEst4VH%2Bq0Zqk%2B6J%2BYViRNM84qI6O4eBd2')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>M58E</td>
                                                <td>MIDAMER-ELEC</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>M58G</td>
                                                <td>MIDAMER-GAS</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242221556</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/09/24 14:08 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/14/24 06:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/14/24 06:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">iajoseph</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">1 WEEKS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">iajoseph</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/08/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242221556&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">PETE WILCOX</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-230-0787</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">PETE WILCOX TRENCHING</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-230-0787</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">1019  LINCOLN ST   CEDAR FALLS, IA  50613</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> Y&nbsp;
                            <b>After 5:00:</b>Y&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line">PETE WILCOX</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">INSTALLING DRAIN TILE</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">MCGEE CONSTRUCTION</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">Y</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Address:</span>
                                <span class="display-line">
                                    2929
                                    
                                    WATERBURY DR
                                </span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">LEXINGTON DR</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">MARK WHERE THE FLAGS ARE ON THE EAST SIDE OF THE HOUSE TO THE CURB.</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5211228, -92.4821958 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5218239, -92.4821831 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5218145, -92.4805737 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5211464, -92.4807454 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=vyyBJmNVNuNH0DfyQdGP0vDhLQ9OROnEst4VH%2Bq0ZqlUS%2FvNh9tRxs4YFj%2BimGza')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242230148</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/10/24 12:22 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/15/24 08:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/15/24 08:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">3 DAYS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/08/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242230148&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">ANDY OTT</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-883-9134</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">SSPI SOLUTIONS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-883-9134</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">1401  EBONY    WAVERLY, IA  50677</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    info@sspi-solutions.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line">ANDY OTT</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-239-2185</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">LANDSCAPING</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">SSPI SOLUTIONS</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">Y</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">Y</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Address:</span>
                                <span class="display-line">
                                    2014
                                    
                                    W 8TH ST
                                </span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">BARRINGTON DR</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">THIS TICKET CONTAINS 2 CIRCLES. THE CENTER OF ALL TWO CIRCLES ARE LOCATED AT 2014 W 8TH ST. 

MARKING INSTRUCTIONS: MARK A 15 FT RADIUS AROUND THE TWO.  EAST MARK, WE ARE REMOVING THOSE 3 PINE TREES, WEST MARK WE ARE REMOVING 1 CRABAPPLE TREE.  WE ARE GRINDING THE STUMPS OUT FOR ALL OF THEM</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302521, -92.4696248 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302450, -92.4696267 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302382, -92.4696298 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302318, -92.4696341 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302259, -92.4696395 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302205, -92.4696460 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302158, -92.4696533 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302118, -92.4696613 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302086, -92.4696701 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302063, -92.4696793 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302049, -92.4696888 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302044, -92.4696985 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302049, -92.4697082 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302063, -92.4697177 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302086, -92.4697269 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302118, -92.4697357 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302158, -92.4697437 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302205, -92.4697510 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302259, -92.4697575 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302318, -92.4697629 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302382, -92.4697672 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302450, -92.4697703 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302521, -92.4697722 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302592, -92.4697728 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302663, -92.4697722 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302734, -92.4697703 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302802, -92.4697672 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302866, -92.4697629 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302925, -92.4697575 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302979, -92.4697510 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303026, -92.4697437 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303066, -92.4697357 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303098, -92.4697269 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303121, -92.4697177 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303135, -92.4697082 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303140, -92.4696985 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303135, -92.4696888 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303121, -92.4696793 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303098, -92.4696701 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303066, -92.4696613 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303026, -92.4696533 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302979, -92.4696460 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302925, -92.4696395 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302866, -92.4696341 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302802, -92.4696298 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302734, -92.4696267 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302663, -92.4696248 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302592, -92.4696242 )
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 2:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303005, -92.4699413 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302934, -92.4699432 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302866, -92.4699463 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302802, -92.4699506 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302743, -92.4699560 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302689, -92.4699625 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302642, -92.4699698 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302602, -92.4699778 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302570, -92.4699866 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302547, -92.4699958 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302533, -92.4700053 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302528, -92.4700150 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302533, -92.4700247 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302547, -92.4700342 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302570, -92.4700434 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302602, -92.4700522 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302642, -92.4700602 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302689, -92.4700675 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302743, -92.4700740 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302802, -92.4700794 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302866, -92.4700837 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5302934, -92.4700868 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303005, -92.4700887 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303076, -92.4700893 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303147, -92.4700887 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303218, -92.4700868 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303286, -92.4700837 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303350, -92.4700794 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303409, -92.4700740 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303463, -92.4700675 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303510, -92.4700602 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303550, -92.4700522 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303582, -92.4700434 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303605, -92.4700342 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303619, -92.4700247 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303624, -92.4700150 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303619, -92.4700053 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303605, -92.4699958 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303582, -92.4699866 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303550, -92.4699778 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303510, -92.4699698 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303463, -92.4699625 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303409, -92.4699560 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303350, -92.4699506 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303286, -92.4699463 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303218, -92.4699432 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303147, -92.4699413 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5303076, -92.4699407 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=Ij5fx%2Ft1uqiExlPXCqzIyfDhLQ9OROnEst4VH%2Bq0ZqnBBB2vWhhTLIgeRbtcE0uD')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242240195</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/11/24 14:49 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/15/24 06:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/15/24 06:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">wiallyn</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">2 WEEK</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">wiallyn</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/08/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242240195&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">SAMMY DANIELS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-961-1659</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">DANIELS CONCRETE CONSTRUCTION</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-961-1659</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">3358  BRISTOL ROAD   WATERLOO, IA  50701</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> Y&nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    DANIELSCONCRETECONSTRUCTIONCO@YAHOO.COM
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line">SAMMY DANIELS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">REPLACE SIDEWALK</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">UNIVERSTIY OF NORTHERN IOWA</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">Y</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">Y</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Address:</span>
                                <span class="display-line">
                                    1402
                                    
                                    W 23RD ST
                                </span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">CAMPUS ST</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">MARK WITHIN THE WHITE FLAGGED AREA LOCATED IN BETWEEN THE LAWTHER HALL BUILDING AND PARKING LOT FOR THE STUDENT HEALTH CENTER ON THE NE CORNER OF THE PARKING LOT OFF W 23R ST</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5160782, -92.4615309 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5160861, -92.4637249 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5167227, -92.4637410 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5169322, -92.4637732 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5169085, -92.4614880 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=JYDIgowp0N3Ch1ShJ1sABPDhLQ9OROnEst4VH%2Bq0ZqkOGvfcv6ZFFsOyNT9fuaYP')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>ICN</td>
                                                <td>IOWA COMMUNICATIONS NETWORK</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>UNI</td>
                                                <td>UNIVERSITY OF NORTHERN IOWA</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242240202</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/11/24 14:59 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/15/24 06:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/15/24 06:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">wiallyn</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">2 WEEK</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">wiallyn</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/08/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242240202&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">SAMMY DANIELS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-961-1659</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">DANIELS CONCRETE CONSTRUCTION</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-961-1659</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">3358  BRISTOL ROAD   WATERLOO, IA  50701</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> Y&nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    DANIELSCONCRETECONSTRUCTIONCO@YAHOO.COM
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line">SAMMY DANIELS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">REPLACE SIDEWALK</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">UNIVERSTIY OF NORTHERN IOWA</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">Y</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">Y</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Address:</span>
                                <span class="display-line">
                                    2300
                                    
                                    INDIANA ST
                                </span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">W 23RD ST</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">MARK WITHIN THE WHITE LINED AREA LOCATED ON THE NE CORNER OF SCHINDLER EDUCATION CENTER BUILDING</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5149325, -92.4618753 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5149721, -92.4644181 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5164667, -92.4643215 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5164667, -92.4621221 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=w5%2BCfVVgBRzj73N0t%2FeQpPDhLQ9OROnEst4VH%2Bq0ZqlLDMjRLONKDdKS%2B5lOdGcz')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>ICN</td>
                                                <td>IOWA COMMUNICATIONS NETWORK</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>UNI</td>
                                                <td>UNIVERSITY OF NORTHERN IOWA</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242240272</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/11/24 17:41 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/15/24 06:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/15/24 06:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">20 WEEKS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/09/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242240272&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">STEVE ADAIR</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-345-2713</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">PETERSON CONTRACTORS INC.</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-345-2713</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">104  BLACKHAWK    REINBECK, IA  50669</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    sadair@petersoncontractors.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line">PCI</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-415-5202</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">SANITARY SEWER</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">PCI</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Work is on or along:</span>
                                <span class="display-line">MAIN ST</span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">16TH ST</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">ROW TO ROW</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249860, -92.4456494 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5249702, -92.4454241 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5240530, -92.4454133 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5240530, -92.4452149 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5239423, -92.4452256 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5239423, -92.4454133 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5230923, -92.4454294 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5230883, -92.4456386 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=UGx8E5zd2khBhkz4mTVLDPDhLQ9OROnEst4VH%2Bq0ZqknH%2B4AXoOGswm%2FSgAH56sp')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CLECIA</td>
                                                <td>WINDSTREAM ENTERPRISE</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242240336</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/11/24 19:55 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/15/24 06:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/15/24 06:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr9</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr9</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/09/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242240336&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">HUNTER KELLY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">563-422-8282</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">SELF</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">563-422-8282</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">3029  COTTONWOOD LN   CEDAR FALLS, IA  50613</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> &nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>Y&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    kellyhunter24@gmail.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">REPAIR FENCE</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">HUNTER KELLY</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">Y</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">Y</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Address:</span>
                                <span class="display-line">
                                    3029
                                    
                                    COTTONWOOD LN
                                </span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">SCENIC DR</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">WEST SIDE OF HOUSE WHERE PART OF EXISTING FENCE IS.</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5144328, -92.4078770 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5144341, -92.4082260 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5148979, -92.4082267 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.5148970, -92.4078700 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=snfc%2Fl9kfHPKSecCe%2Fm7mPDhLQ9OROnEst4VH%2Bq0ZqkimQXKR5J7TxO%2F9IpA4jqG')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>M58E</td>
                                                <td>MIDAMER-ELEC</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>M58G</td>
                                                <td>MIDAMER-GAS</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242240361</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/11/24 20:42 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/15/24 06:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/15/24 06:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr9</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">1 DAY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr9</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/09/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242240361&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">CRAIG LARSEN</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-269-3310</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">CRAIG LARSEN CONSTRUCTION</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-269-3310</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">220  WEST LONE TREE ROAD   CEDAR FALLS, IA  50613</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> &nbsp;
                            <b>PM:</b> Y&nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    craig.lars.larsen@gmail.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">POST HOLES FOR DECK</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">CRAIG LARSEN</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">Y</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Address:</span>
                                <span class="display-line">
                                    5414
                                    
                                    HEDGEWOOD CIRCLE
                                </span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">BOXWOOD DRIVE</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">NORTHEAST CORNER OF LOT</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4889496, -92.4730721 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4890005, -92.4731491 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4890164, -92.4732242 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4893967, -92.4733790 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4893958, -92.4727857 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4893163, -92.4726467 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=3zcZA17j6BS0SRHkvcHPJfDhLQ9OROnEst4VH%2Bq0ZqmzPMNsSOM5X16beKEqNpvS')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242240384</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/11/24 21:24 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/15/24 08:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/15/24 08:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">1 DAY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/09/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242240384&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">CINDY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-277-5579</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">WEBER ELECTRIC INC</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-277-5579</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">5810  PRAIRIE    CEDAR FALLS, IA  50613</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> Y&nbsp;
                            <b>After 5:00:</b>Y&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    larcin@cfu.net
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line">WEBER ELECTRIC INC</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-240-2680</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">TRENCH</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">WEBER ELECTRIC INC</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">Y</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS TWP</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">N</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Address:</span>
                                <span class="display-line">
                                    6616
                                    
                                    VIKING RD
                                </span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">INNOVATION DR</span>
                                </div>
                                
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Township:</span>
                                <span class="display-line">CEDAR FALLS TWP</span>
                            </div>
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Section, Qtr Section:</span>
                                <span class="display-line">27-SW</span>
                            </div>
                            

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">MARKING INSTRUCTIONS: MARK 1 FT EITHER SIDE OF THE FLAGGED ROUTE - FROM METER BOARD TO NEW HOUSE.. MARK FOLLOWING THE ROUTE S FOR 55 FT.
FROM THE INTERSECTION OF VIKING RD AND INNOVATION DR, HEAD NORTH FOR 0.121 MI HEAD W FOR 111 FT TO THE BEGINNING OF THE ROUTE.</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4856946, -92.4879590 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4856673, -92.4879548 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4856611, -92.4880285 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4858368, -92.4880554 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4858641, -92.4880596 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4858703, -92.4879859 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=L0MD4Kce9zmQvQk7I8XsM%2FDhLQ9OROnEst4VH%2Bq0ZqlWds6fFtscVeuTFm3N%2F3Pu')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF1</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242250153</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/12/24 07:22 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/15/24 08:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/15/24 08:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">20 DAYS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/09/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242250153&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">DUSTIN</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-269-4990</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">ARENDS &amp; SONS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-269-4990</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">33498  110TH    CEDAR FALLS, IA  50613</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> &nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    darends123@aol.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">SITE WORK</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">RICE COMPANIES</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS TWP</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">N</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Work is on or along:</span>
                                <span class="display-line">TECHNOLOGY PKWY</span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">INNOVATION DR</span>
                                </div>
                                
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Township:</span>
                                <span class="display-line">CEDAR FALLS TWP</span>
                            </div>
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Section, Qtr Section:</span>
                                <span class="display-line">34-SW</span>
                            </div>
                            

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">MARKING INSTRUCTIONS: MARK ENTIRE PROPERTY.
FROM THE INTERSECTION OF TECHNOLOGY PKWY AND INNOVATION DR, HEAD WEST ON TECHNOLOGY PKWY FOR 157 FT TO THE SITE ON THE N SIDE OF THE STREET.</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line">ADDITIONAL TSQ: CEDAR FALLS TWP S-34NW ADDITIONAL TSQ: CEDAR FALLS TWP S-34NW
  RELOCATE: CUSTOMER IS NOT REQUESTING ANY UTILITIES REMARK THEIR FACILITIES FOR THIS RELOCATE.  RELOCATE REASON: AREA TO BE MARKED WITH PAINT AND FLAGS ATTACHMENTS: NO </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4768159, -92.4881719 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4768172, -92.4865950 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4760401, -92.4865929 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4760211, -92.4865949 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4760027, -92.4866011 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4759853, -92.4866112 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4759693, -92.4866250 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4759551, -92.4866422 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4759432, -92.4866622 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4759339, -92.4866846 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4759274, -92.4867087 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4759239, -92.4867339 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4759092, -92.4869215 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4759065, -92.4869274 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4759044, -92.4869337 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4759032, -92.4869404 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4759028, -92.4869472 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4759031, -92.4869541 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4759043, -92.4869608 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4759165, -92.4871231 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4759340, -92.4872845 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4759567, -92.4874447 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4759847, -92.4876035 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4760178, -92.4877603 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4761761, -92.4884525 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4761911, -92.4884459 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=lg%2F91zunfSDw4O4rWlEwV%2FDhLQ9OROnEst4VH%2Bq0Zql2wzYyp%2FljUwYpfPkOahAz')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">242250171</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/12/24 07:22 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">COMPLIANT</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/15/24 08:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/15/24 08:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line">1 WEEK</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr6</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/09/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=242250171&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">DUSTIN</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-269-4990</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">ARENDS &amp; SONS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-269-4990</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">33498  110TH    CEDAR FALLS, IA  50613</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> Y&nbsp;
                            <b>After 5:00:</b>Y&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    darends123@aol.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">DIG UP TANKS FOR WATERPROOFING</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">TARGET</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line">Y</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line">N</span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line">N</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Address:</span>
                                <span class="display-line">
                                    2200
                                    
                                    VIKING ROAD
                                </span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">HUDSON ROAD</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">LOCATE AREA INSIDE THE POLYGON</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4838468, -92.4679012 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4838389, -92.4673621 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4834631, -92.4673594 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4834670, -92.4679093 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=dUhuOcK95OUrGb%2FgXutPafDhLQ9OROnEst4VH%2Bq0ZqmfllHCch8BeasX1%2Bh4sXZS')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded - Excavator has selected dynamic start option</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CLECIA</td>
                                                <td>WINDSTREAM ENTERPRISE</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">552404776</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/08/24 13:15 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">DESIGN LOCATE</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/16/24 07:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/16/24 07:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/07/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=552404776&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">WADE WAMRE</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">SHIVE-HATTERY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">316  2ND ST SE SUITE 500    CEDAR RAPIDS, IA  52406</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    wwamre@shive-hattery.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">DESIGN INFORMATION</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">CITY OF CEDAR FALLS </span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Work is on or along:</span>
                                <span class="display-line">WEST RIDGEWAY AVENUE</span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">HUDSON ROAD</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">LOOKING FOR ANY EXISTING UTILIZES IN THE AREA. THANK YOU</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4679953, -92.4659736 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4665163, -92.4659736 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4654416, -92.4687398 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4652735, -92.4694640 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4651983, -92.4703062 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4651966, -92.4709037 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4679953, -92.4709037 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=MM1%2B98Ozo4M7YZibYkS78fDhLQ9OROnEst4VH%2Bq0ZqnSqKdRZQudxiAyTlZJUETk')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>UPN</td>
                                                <td>UNITE PRIVATE NETWORKS, LLC</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>W19</td>
                                                <td>IOWA DEPARTMENT OF TRANSPORTAT</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">552404777</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/08/24 13:15 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">DESIGN LOCATE</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/16/24 07:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/16/24 07:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/07/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=552404777&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">WADE WAMRE</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">SHIVE-HATTERY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">316  2ND ST SE SUITE 500    CEDAR RAPIDS, IA  52406</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    wwamre@shive-hattery.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line">WADE WAMRE</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-361-6314</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">DESIGN INFORMATION</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">CITY OF CEDAR FALLS </span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Work is on or along:</span>
                                <span class="display-line">WEST RIDGEWAY AVENUE</span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">HUDSON ROAD</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">LOOKING FOR ANY EXISTING UTILIZES IN THE AREA. THANK YOU</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4696935, -92.4709037 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4697171, -92.4660423 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4707934, -92.4659886 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4707940, -92.4659736 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4679953, -92.4659736 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4679953, -92.4709037 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=hmCy9Z5mO7F%2BK3aKyAYcnvDhLQ9OROnEst4VH%2Bq0ZqlLY82oN4ezM9TD4z6ziyQ4')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CLECIA</td>
                                                <td>WINDSTREAM ENTERPRISE</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>GDC</td>
                                                <td>GRUNDY CENTER MUNICIPAL UTILIT</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>UPN</td>
                                                <td>UNITE PRIVATE NETWORKS, LLC</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">552404778</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/08/24 13:15 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">DESIGN LOCATE</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/16/24 07:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/16/24 07:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/07/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=552404778&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">WADE WAMRE</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">SHIVE-HATTERY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">316  2ND ST SE SUITE 500    CEDAR RAPIDS, IA  52406</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    wwamre@shive-hattery.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">DESIGN INFORMATION</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">CITY OF CEDAR FALLS </span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Work is on or along:</span>
                                <span class="display-line">WEST RIDGEWAY AVENUE</span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">HUDSON ROAD</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">LOOKING FOR ANY EXISTING UTILIZES IN THE AREA. THANK YOU</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4707940, -92.4659736 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4708250, -92.4652484 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4697171, -92.4651947 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4696985, -92.4610436 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4679848, -92.4610436 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4679848, -92.4659736 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=lu2EXcWNBUb0YUdsVSPSmPDhLQ9OROnEst4VH%2Bq0ZqlG%2FvusHZMbLtLf8nwURO%2B8')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CLECIA</td>
                                                <td>WINDSTREAM ENTERPRISE</td>
                                        
                                                <td>Marked</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>GDC</td>
                                                <td>GRUNDY CENTER MUNICIPAL UTILIT</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>UPN</td>
                                                <td>UNITE PRIVATE NETWORKS, LLC</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">552404779</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/08/24 13:15 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">DESIGN LOCATE</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/16/24 07:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/16/24 07:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/07/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=552404779&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">WADE WAMRE</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">SHIVE-HATTERY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">316  2ND ST SE SUITE 500    CEDAR RAPIDS, IA  52406</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> Y&nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    wwamre@shive-hattery.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">DESIGN INFORMATION</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">CITY OF CEDAR FALLS </span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Work is on or along:</span>
                                <span class="display-line">WEST RIDGEWAY AVENUE</span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">HUDSON ROAD</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">LOOKING FOR ANY EXISTING UTILIZES IN THE AREA. THANK YOU</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4652296, -92.4758338 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695430, -92.4758150 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695430, -92.4752600 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695430, -92.4751120 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4696730, -92.4751106 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4696935, -92.4709037 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4651966, -92.4709037 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4651938, -92.4718454 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=3d7waq7emRXo%2B0qIth8IY%2FDhLQ9OROnEst4VH%2Bq0ZqlNiceABITArCu57MoDyqtc')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF1</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>GDC</td>
                                                <td>GRUNDY CENTER MUNICIPAL UTILIT</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">552404779</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/08/24 13:15 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">DESIGN LOCATE</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/16/24 07:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/16/24 07:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/07/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=552404779&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">WADE WAMRE</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">SHIVE-HATTERY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">316  2ND ST SE SUITE 500    CEDAR RAPIDS, IA  52406</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> Y&nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    wwamre@shive-hattery.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">DESIGN INFORMATION</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">CITY OF CEDAR FALLS </span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Work is on or along:</span>
                                <span class="display-line">WEST RIDGEWAY AVENUE</span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">HUDSON ROAD</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">LOOKING FOR ANY EXISTING UTILIZES IN THE AREA. THANK YOU</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4652296, -92.4758338 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695430, -92.4758150 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695430, -92.4752600 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695430, -92.4751120 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4696730, -92.4751106 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4696935, -92.4709037 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4651966, -92.4709037 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4651938, -92.4718454 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=3d7waq7emRXo%2B0qIth8IY%2FDhLQ9OROnEst4VH%2Bq0Zqn1fRKUhDZ%2BOUDwEbKotJCM')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF1</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>GDC</td>
                                                <td>GRUNDY CENTER MUNICIPAL UTILIT</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">552404780</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/08/24 13:15 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">DESIGN LOCATE</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/16/24 07:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/16/24 07:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/07/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=552404780&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">WADE WAMRE</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">SHIVE-HATTERY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">316  2ND ST SE SUITE 500    CEDAR RAPIDS, IA  52406</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    wwamre@shive-hattery.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">DESIGN INFORMATION</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">CITY OF CEDAR FALLS </span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Work is on or along:</span>
                                <span class="display-line">WEST RIDGEWAY AVENUE</span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">HUDSON ROAD</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">LOOKING FOR ANY EXISTING UTILIZES IN THE AREA. THANK YOU</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4696985, -92.4610436 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4696764, -92.4561135 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4673186, -92.4561192 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4673186, -92.4610436 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=cs8AQODTucHy3sCgF3B11fDhLQ9OROnEst4VH%2Bq0ZqnnSRwBNiZICGO8rqNWVhYy')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CLECIA</td>
                                                <td>WINDSTREAM ENTERPRISE</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">552404781</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/08/24 13:15 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">DESIGN LOCATE</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/16/24 07:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/16/24 07:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/07/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=552404781&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">WADE WAMRE</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">SHIVE-HATTERY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">316  2ND ST SE SUITE 500    CEDAR RAPIDS, IA  52406</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    wwamre@shive-hattery.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">DESIGN INFORMATION</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">CITY OF CEDAR FALLS </span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Work is on or along:</span>
                                <span class="display-line">WEST RIDGEWAY AVENUE</span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">HUDSON ROAD</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">LOOKING FOR ANY EXISTING UTILIZES IN THE AREA. THANK YOU</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4673186, -92.4561192 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4649387, -92.4561249 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4649753, -92.4583718 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4651336, -92.4609682 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4651447, -92.4610436 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4673186, -92.4610436 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=WXmR%2FpYIWWI99C3Q4mKBG%2FDhLQ9OROnEst4VH%2Bq0ZqmpUy0icanTHhytfcDzoZYz')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">552404782</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/08/24 13:15 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">DESIGN LOCATE</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/16/24 07:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/16/24 07:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/07/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=552404782&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">WADE WAMRE</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">SHIVE-HATTERY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">316  2ND ST SE SUITE 500    CEDAR RAPIDS, IA  52406</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    wwamre@shive-hattery.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">DESIGN INFORMATION</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">CITY OF CEDAR FALLS </span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">BLACK HAWK TWP</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">N</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Work is on or along:</span>
                                <span class="display-line">WEST RIDGEWAY AVENUE</span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">HUDSON ROAD</span>
                                </div>
                                
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Township:</span>
                                <span class="display-line">BLACK HAWK TWP</span>
                            </div>
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Section, Qtr Section:</span>
                                <span class="display-line">4-NE</span>
                            </div>
                            

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">LOOKING FOR ANY EXISTING UTILIZES IN THE AREA. THANK YOU</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line">ADDITIONAL TSQ: BLACK HAWK TWP S-34SE,BLACK HAWK TWP S-3NW </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695431, -92.4761294 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695430, -92.4760140 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695430, -92.4758150 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4652296, -92.4758338 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4652333, -92.4762442 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=fRQ6Gfe5FS6odoPNxID%2FrvDhLQ9OROnEst4VH%2Bq0Zqk77MHA%2FpOEKO4m4TIp%2Fx9x')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF1</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>GDC</td>
                                                <td>GRUNDY CENTER MUNICIPAL UTILIT</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">552404782</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/08/24 13:15 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">DESIGN LOCATE</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/16/24 07:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/16/24 07:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/07/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=552404782&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">WADE WAMRE</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">SHIVE-HATTERY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">316  2ND ST SE SUITE 500    CEDAR RAPIDS, IA  52406</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    wwamre@shive-hattery.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">DESIGN INFORMATION</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">CITY OF CEDAR FALLS </span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">BLACK HAWK TWP</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">N</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Work is on or along:</span>
                                <span class="display-line">WEST RIDGEWAY AVENUE</span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">HUDSON ROAD</span>
                                </div>
                                
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Township:</span>
                                <span class="display-line">BLACK HAWK TWP</span>
                            </div>
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Section, Qtr Section:</span>
                                <span class="display-line">4-NE</span>
                            </div>
                            

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">LOOKING FOR ANY EXISTING UTILIZES IN THE AREA. THANK YOU</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line">ADDITIONAL TSQ: BLACK HAWK TWP S-34SE,BLACK HAWK TWP S-3NW </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695431, -92.4761294 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695430, -92.4760140 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695430, -92.4758150 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4652296, -92.4758338 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4652333, -92.4762442 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=fRQ6Gfe5FS6odoPNxID%2FrvDhLQ9OROnEst4VH%2Bq0ZqllUiyBlz6QBvzloHigIoHG')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF1</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>GDC</td>
                                                <td>GRUNDY CENTER MUNICIPAL UTILIT</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">552404783</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/08/24 13:15 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">DESIGN LOCATE</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/16/24 07:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/16/24 07:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/07/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=552404783&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">WADE WAMRE</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">SHIVE-HATTERY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">316  2ND ST SE SUITE 500    CEDAR RAPIDS, IA  52406</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    wwamre@shive-hattery.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">DESIGN INFORMATION</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">CITY OF CEDAR FALLS </span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">Y</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Work is on or along:</span>
                                <span class="display-line">WEST RIDGEWAY AVENUE</span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">HUDSON ROAD</span>
                                </div>
                                

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">LOOKING FOR ANY EXISTING UTILIZES IN THE AREA. THANK YOU</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line"> </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4679848, -92.4610436 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4651447, -92.4610436 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4652642, -92.4618587 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4655055, -92.4627224 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4665937, -92.4653978 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4665462, -92.4658966 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4665163, -92.4659736 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4679848, -92.4659736 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=0AoLA7gKkiBUFj6NRxaXQfDhLQ9OROnEst4VH%2Bq0Zqlx2zRI9qfILKoJY5ffstsl')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>UPN</td>
                                                <td>UNITE PRIVATE NETWORKS, LLC</td>
                                        
                                                <td>Clear</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>W19</td>
                                                <td>IOWA DEPARTMENT OF TRANSPORTAT</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">552404784</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/08/24 13:15 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">DESIGN LOCATE</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/16/24 07:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/16/24 07:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/07/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=552404784&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">WADE WAMRE</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">SHIVE-HATTERY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">316  2ND ST SE SUITE 500    CEDAR RAPIDS, IA  52406</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    wwamre@shive-hattery.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">DESIGN INFORMATION</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">CITY OF CEDAR FALLS </span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS TWP</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">N</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Work is on or along:</span>
                                <span class="display-line">WEST RIDGEWAY AVENUE</span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">HUDSON ROAD</span>
                                </div>
                                
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Township:</span>
                                <span class="display-line">CEDAR FALLS TWP</span>
                            </div>
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Section, Qtr Section:</span>
                                <span class="display-line">34-SE</span>
                            </div>
                            

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">LOOKING FOR ANY EXISTING UTILIZES IN THE AREA. THANK YOU</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line">ADDITIONAL TSQ: CEDAR FALLS TWP S-35SW ADDITIONAL TSQ: CEDAR FALLS TWP S-35SW </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4696730, -92.4751106 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695430, -92.4751120 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695430, -92.4752600 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695430, -92.4758150 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695430, -92.4760140 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695431, -92.4761294 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4696681, -92.4761261 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=97UEVEUtDdANt3HeBKmpd%2FDhLQ9OROnEst4VH%2Bq0ZqnOOXeI7inXWvnCg%2BoZMuUF')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF1</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>GDC</td>
                                                <td>GRUNDY CENTER MUNICIPAL UTILIT</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
            


                <h1 style="text-align:center;">Iowa One Call</h1>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Ticket No:</span>
                        <span class="display-line">552404784</span>
                    </div>
                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span style="color:red">&nbsp;</span>
                            </div>
                            
                            



                            

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Original Call Date:</span>
                        <span class="display-line">08/08/24 13:15 pm</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">&nbsp;</span>
                        <span class="">DESIGN LOCATE</span>
                    </div>
                    
                        <div class="pure-u-md-1-1 pure-u-1-1">
                            <span class="display-line-label">Locates shall be completed no later than:</span>
                            <span class="display-line">08/16/24 07:00 am</span>
                        </div>
                        
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Beginning Work Date:</span>
                        <span class="display-line">08/16/24 07:00 am</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Duration:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Op:</span>
                        <span class="display-line">webusr70</span>
                    </div>

                    
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Expiration Date:</span>
                                <span class="display-line">09/07/24</span>
                            </div>
                            
                </div> 

                <div class="noprint">
                    <div class="blank-separator"></div>
                    <div class="heading">TICKET ACTIONS</div>
                    <div class="separator noprint"></div>

                    
                                <span>
                                    <input class="button link" type="button" value="Add Public Attachment" title="Add Public Attachment" onclick="location.href='attachFile.jsp?msgNumber=552404784&amp;revNumber=0&amp;key=null&amp;db=ia&amp;ltm=n&amp;etm=n&amp;cid=90&amp;stateName=IA&amp;rec=null'">
                                </span>
                                
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">CALLER INFORMATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Caller Name:</span>
                        <span class="display-line">WADE WAMRE</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavator Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Excavator Name:</span>
                        <span class="display-line">SHIVE-HATTERY</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line">319-364-0227</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Address:</span>
                        <span class="display-line">316  2ND ST SE SUITE 500    CEDAR RAPIDS, IA  52406</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Fax Phone:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Best Time:</span>
                        <span class="display-line">
                            <b>AM:</b> Y&nbsp;
                            <b>PM:</b> &nbsp;
                            <b>After 5:00:</b>&nbsp;
                        </span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Contact Email:</span>
                        <span class="display-line">
                            
                                    wwamre@shive-hattery.com
                                    
                        </span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Onsite Contact:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">Phone:</span>
                        <span class="display-line"></span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">Excavation Information</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Type of Work:</span>
                        <span class="display-line">DESIGN INFORMATION</span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Work Being Done For:</span>
                        <span class="display-line">CITY OF CEDAR FALLS </span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Trenching:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Boring:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Plowing:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Backhoe:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Blasting:</span>
                        <span class="display-line"></span>
                    </div>
                    <div class="pure-u-md-1-3 pure-u-1-1">
                        <span class="display-line-label">Other:</span>
                        <span class="display-line"></span>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Marked in White:</span>
                        <span class="display-line">N</span>
                    </div>
                </div> 

                <div class="blank-separator"></div>
                <div class="heading">DIG SITE LOCATION</div>
                <div class="separator noprint"></div>

                <div class="pure-g">
                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">County:</span>
                        <span class="display-line">BLACK HAWK</span>
                    </div>

                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City:</span>
                        <span class="display-line">CEDAR FALLS TWP</span>
                    </div>
                    <div class="pure-u-md-1-2 pure-u-1-1">
                        <span class="display-line-label">City Limits:</span>
                        <span class="display-line">N</span>
                    </div>

                    
                            <div class="pure-u-md-1-1 pure-u-1-1">
                                <span class="display-line-label">Work is on or along:</span>
                                <span class="display-line">WEST RIDGEWAY AVENUE</span>
                            </div>
                            
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <span class="display-line-label">At:</span>
                                    <span class="display-line">HUDSON ROAD</span>
                                </div>
                                
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Township:</span>
                                <span class="display-line">CEDAR FALLS TWP</span>
                            </div>
                            <div class="pure-u-md-1-2 pure-u-1-1">
                                <span class="display-line-label">Section, Qtr Section:</span>
                                <span class="display-line">34-SE</span>
                            </div>
                            

                    <div class="pure-u-1-1">
                        <table>
                            <tbody>
                                <tr>
                                    <td class="display-line-label">Location of Work:</td>
                                    <td class="display-line"><span style="white-space: pre-wrap;">LOOKING FOR ANY EXISTING UTILIZES IN THE AREA. THANK YOU</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="pure-u-md-1-1 pure-u-1-1">
                        <span class="display-line-label">Remarks:</span>
                        <span class="display-line">ADDITIONAL TSQ: CEDAR FALLS TWP S-35SW ADDITIONAL TSQ: CEDAR FALLS TWP S-35SW </span>
                    </div>
                </div> 

                
                <b>Coordinates for each location:</b>
                <div class="pure-g">
                    
                                <div class="pure-u-md-1-1 pure-u-1-1">
                                    <b>Polygon 1:</b>
                                </div>
                                
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4696730, -92.4751106 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695430, -92.4751120 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695430, -92.4752600 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695430, -92.4758150 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695430, -92.4760140 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4695431, -92.4761294 )
                            </div>
                            
                            <div class="pure-u-md-1-3 pure-u-1-1">
                                ( 42.4696681, -92.4761261 )
                            </div>
                            
                </div> 

                
                
            <div class="blank-separator"></div>
            <div class="heading">MEMBERS NOTIFIED</div>
            <div class="separator noprint"></div>

            <table class="transparent">
                <thead>
                                    <tr>
                                                <th>&nbsp;</th>
                                                <th>District</th>
                                                <th>Company Name</th>
                        
                                                <th>Status</th>
                                                <th>
                                                    <span>
                                        
                                                    
                                                        <input class="button link noprint" type="button" value="Status History" onclick="javascript:popup('ticketStatusHistory.jsp?enc=97UEVEUtDdANt3HeBKmpd%2FDhLQ9OROnEst4VH%2Bq0ZqlCR48EhMiR%2FKCC7mEKsVYA')">
                                        
                                                    </span>
                                                </th>
                                
                                    </tr>
                </thead>
                <tbody>
                    
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>AT6</td>
                                                <td>MEDIACOM</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF1</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF2</td>
                                                <td>CEDAR FALLS UTILITIES</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CF4</td>
                                                <td>CEDAR FALLS, CITY OF</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>CTLIA01</td>
                                                <td>CENTURYLINK</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                                    <tr>
                                                <td>&nbsp;</td>
                                                <td>GDC</td>
                                                <td>GRUNDY CENTER MUNICIPAL UTILIT</td>
                                        
                                                <td>Not yet responded</td>
                                                
                                    </tr>
                                
                </tbody>
            </table>
            

           	
           		<div class="page-break"></div>
                
    
       
    
        
        </div> 
        <div class="footer-push"></div>
        </div> 
    <footer><span class="copyright"></span></footer>        
  

<style>body.tablesorter-disableSelection { -ms-user-select: none; -moz-user-select: -moz-none;-khtml-user-select: none; -webkit-user-select: none; user-select: none; }.tablesorter-resizable-container { position: relative; height: 1px; }.tablesorter-resizable-handle { position: absolute; display: inline-block; width: 8px; top: 1px;cursor: ew-resize; z-index: 3; user-select: none; -moz-user-select: none; }</style></body></html>

"""