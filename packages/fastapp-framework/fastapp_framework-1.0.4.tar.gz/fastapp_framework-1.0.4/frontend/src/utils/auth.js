

const doAuthFetch = async (url, config, fastapp_token, removeCookies, redir = null) => {

    if (fastapp_token === undefined || fastapp_token === null
        || fastapp_token.access_token === undefined || fastapp_token.access_token === null) {
        if(redir !== null){
            window.location.replace("/login?redir=" + redir);
        }
        return {status: "error", message: "Token undefined"}
    }

    if('headers' in config){
        config.headers.Authorization = `Bearer ${fastapp_token.access_token}`
    } else {
        config.headers = {
            Authorization: `Bearer ${fastapp_token.access_token}`
        }
    }

    const data = await fetch(url, config)
    .then(async response => {
        const data = await response.json();
        console.log("Response: ", data);

        if(response.status === 401){
            if(data.detail === "Invalid token" || 
                data.detail === "Token has expired" ||
                data.detail === "User not found"
            ){
                // Current token in cookies is bad remove it
                removeCookies('fastapp_token');
                if(redir !== null){
                    window.location.replace("/login?redir=" + redir);
                }
            } else {
                console.error("Request Error: ", data.message);
                return {};
            }

        } else if(response.status >= 400){
            console.error("Request Error: ", data.message);
            return {status: "error", message: "Request failed"};
        }
        
        return {
            status: "success",
            data: data
        };
    })
    .catch(error => {
        console.error(error);
        if(redir !== null){
            window.location.replace("/login?redir=" + redir);
        }
        return {status: "error", message: "Request failed"};
    });

    return data;
}

export {doAuthFetch};