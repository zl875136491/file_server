$(document).ready(function() {

    $("#sample_1").dataTable(
        {
            searching : false,
            destroy : true,

            columns: [
                { },
                { 'file_name' },
                { 'file_owner' },
                { 'upload_date' },
            ],
            'columnDefs': [{
                'targets': 0,
                'searchable': false,
                'orderable': false,
                'className': 'select-checkbox',
                'render': function (data, type, full, meta){
                return  '<label class="mt-checkbox mt-checkbox-single mt-checkbox-outline"><input type="checkbox" class="checkboxes" value="1"/><span></span></label>'
                }
            }],

         }

    );
});