/*  Gen By Xiaok  */
function reload_dhcp(force) {
    $.ajax({
                    type: "GET",
                    url: "/public/api",
                    data: { "module":"dhcp","fun":"reload","value":force},
                    dataType: "text",
                    success: function(msg){
                        if (msg == "2") {
                            alert("{{ _('DHCP configuration loaded successfully') }}");
                            location.reload();
                        } else if (msg == "1") {
                            if ( confirm("{{ _('Configuration MD5 validation failed, override?') }}") ) {
                                reload_dhcp("force");
                                return true;
                            };
                            return false;
                        } else if (msg == "3") {
                            alert("{{ _('Error: Restarting the DNSmasq service failed') }}");
                            return false;
                        } else if (msg == "4") {
                            alert("{{ _('Failed to write DHCP configuration') }}");
                            return false;
                        } else {
                            alert("{{ _('Error: Operation failed for unknown reason') }}");
                            return false;
                        }
                        },
                    error:function(){
                        alert("{{ _('Error: Internal Server Error') }}");
                        return false;
                        },
    });
};
