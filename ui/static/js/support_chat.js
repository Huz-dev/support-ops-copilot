async function sendMessage(){

    const message =
        document.getElementById(
            "message"
        ).value;

    const response =
        await fetch(
            "/support-message",
            {
                method:"POST",

                headers:{
                    "Content-Type":
                    "application/json"
                },

                body:JSON.stringify({
                    message
                })
            }
        );

    const data =
        await response.json();

    document.getElementById(
        "response"
    ).innerHTML =
        JSON.stringify(
            data,
            null,
            2
        );
}