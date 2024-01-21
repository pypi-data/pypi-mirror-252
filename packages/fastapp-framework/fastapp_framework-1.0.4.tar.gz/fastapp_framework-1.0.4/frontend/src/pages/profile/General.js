import { FaClipboard, FaEdit } from "react-icons/fa";
import { useCookies } from "react-cookie";
import { useState, useEffect } from "react";

import { doAuthFetch } from "../../utils/auth";
import { Column, Columns } from "../../components/Columns"

const InfoBox = (props) => {
    return (
        <h3 className="has-text-light"
            style={{border: "1px solid white", padding: "10px", borderRadius: "5px"}}
        >
            <Columns>
                <Column args={"is-10"}>
                    {props.title}: {props.value}
                </Column>
                <Column args={"is-2"}>
                    <a className="mr-4" href="/null" onClick={(e) => {
                        e.preventDefault();
                        navigator.clipboard.writeText(props.value)
                    }}><FaClipboard /></a>
                    <a href="/null" onClick={(e) => {
                        e.preventDefault();
                    }}><FaEdit /></a>
                </Column>
            </Columns>
        </h3>
    )
}

export default function General(props){
    const [cookies, , removeCookies] = useCookies(['fastapp_token']);
    const [userInfo, setUserInfo] = useState({
        name: "",
        email: "",
        first_name: "",
        last_name: ""
    });

    useEffect(() => {
        const getUserInfo = async () => {
            const resp = await doAuthFetch(
                "/api/v1/auth/users/me",
                {
                    method: "GET",
                },
                cookies.fastapp_token,
                removeCookies,
                "/profile"
            );

            if(resp.status === "success"){
                setUserInfo(resp.data);
            } else {
                removeCookies("fastapp_token")
                window.location.replace("/login")
            }
        }
    
        getUserInfo();
    }, [cookies.fastapp_token, removeCookies]);

    return (
        <div className="content">
            <h2 className="subtitle">General Information</h2>
            <Columns args={"is-multiline"}>
                <Column args={"is-6"}>
                    <InfoBox title={"Username"} value={userInfo.name}/>
                </Column>
                <Column args={"is-6"}>
                    <InfoBox title={"Email"} value={userInfo.email}/>
                </Column>
                <Column args={"is-6"}>
                    <InfoBox title={"First Name"} value={userInfo.first}/>
                </Column>
                <Column args={"is-6"}>
                    <InfoBox title={"Last Name"} value={userInfo.last}/>
                </Column>
            </Columns>

            <h2 className="subtitle">User Preferences</h2>
        </div>
    )
}