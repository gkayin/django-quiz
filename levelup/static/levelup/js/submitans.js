$(document).ready(function(){

    $('#button1').on('click', function(event){
 
        event.preventDefault();    

        var selectedAns = $('input[name="vbtn-radio"]:checked').val();

        console.log('selectedAns is ::' + selectedAns); 

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; 

        $.ajax({
                url: '/quiz/',
                type: 'POST',
                accepts: {
                    text: "application/json"
                },
                contentType: 'application/json',

                context:this,
                
                headers: {"X-Requested-With": "XMLHttpRequest","X-CSRFToken": csrftoken},
                
                data: JSON.stringify({"answer":selectedAns, "csrfmiddlewaretoken" : " {{csrf_token}} "}) ,

                success: function(response){  

                    //$("#textArea1").val(selectedAns)

                    console.log('response-status is :: ' + response['Status']);   

                    if (response['Status'] != "error") {

                        console.log('response-status is :: ' + response['Status']);   
                        console.log('selectedAns2 is ::' + selectedAns);
                        console.log('response is ::' + response['answer']);
                        console.log('btn_clicked is ::' + response['btn_clicked']);

                        $('input:radio[name="vbtn-radio"]').each(function () {
                            var idVal = $(this).attr("id");
                            console.log("label is :: " + $("label[for='"+idVal+"']").text());
                            
                            $("label[for='"+idVal+"']").removeClass('btn-outline-warning')

                            if (this.value == response['answer']) {
                                $("label[for='"+idVal+"']").addClass('btn-outline-success');
                                $("label[for='"+idVal+"']").addClass('active');
                                $("label[for='"+idVal+"']").addClass('text-white');
                            }    
                            else {
                                if (this.checked == true) {
                                    $("label[for='"+idVal+"']").addClass('btn-outline-danger');
                                    $("label[for='"+idVal+"']").addClass('text-white');
                                } 
                                else
                                    $("label[for='"+idVal+"']").addClass('btn-outline-warning')    
                            }
                            $("label[for='"+idVal+"']").css({"cursor": "not-allowed", "pointer-events": "none"});
                        });    
        
                        $('input:button[id="button1"]').addClass('disabled');

                        if (selectedAns == response['answer'])
                        {
                            txtarea_str = "Thats right. Answer is " + response['answer']; 
                            $("#textArea1").html(txtarea_str); 
                        }    
                        else
                        {
                            txtarea_str = "Thats wrong. Correct Answer is " + response['answer']; 
                            $("#textArea1").html(txtarea_str);    
                        }
                    } else
                    {
                        $("#textArea1").html("");
                        console.log('response-status-2 is :: ' + response['Status']);   
//                      alert("No Option selected. Please choose one of them");
//                        $("#emsg").html("No Option selected. Please choose one of them");
//                        $("#msgdiv").show();   
//                        $("#result").html("No Option selected. Please choose one of them"); 
//                      $("#result").addClass("alert alert-info alert-dismissible fade show");
//                      $('.alert').alert();
                        $("#result").show('fade'); 
                    }        
                }
                ,
                error: function(error){
                    console.error(error);
                }

              })
              

    });

    $('#linkClose').click(function () {
        console.log('reached here :: ');
        $("#result").hide('fade');
    });
            
})