import { useState } from "react";
import { useCookies } from "react-cookie";

import Outline from "../components/Outline"
import Popup from "../components/Popups"
import { Column, Columns } from "../components/Columns"
import { doAuthFetch } from "../utils/auth";

const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;

const validateEmail = (email) => email.match(emailRegex);

export default function ForgotPass(props){
    const [cookies, , removeCookies] = useCookies(['fastapp_token'])
    const [email, setEmail] = useState('');
    const [failActive, setFailActive] = useState(false);
    const [successActive, setSuccessActive] = useState(false);
    const emailValid = validateEmail(email);

    const reqReset = async (email) => {
        const resp = await fetch('/api/v1/auth/user/reset-password?' + new URLSearchParams({email: email}))

        if(resp !== undefined && resp.status === 200){
            setSuccessActive(true);
            setFailActive(false);
        } else {
            setSuccessActive(false);
            setFailActive(true);
        }
    }

    return (
        <Outline>
            <Columns>
                <Column args={'is-4 is-offset-4'}>
                    <h1 className="title has-text-centered">Reset Password</h1>
                    <p className="has-text-centered">An email will be sent allowing you to change your password</p>
                    <br></br>
                    <div className="field">
                        <label className="label has-text-light">Email</label>
                        <p className="control">
                            <input className={`input ${(email.length !== 0 && !emailValid) ? 'is-danger': ''}`} type="email" placeholder="e.g. me@me.com" onChange={(e) => {
                                e.preventDefault();
                                setEmail(e.target.value);
                            }}></input>
                        </p>
                    </div>
                    <div className="has-text-centered">
                        <button className="button" disabled={!emailValid} onClick={() => reqReset(email)}>Send Reset Email</button>
                    </div>
                </Column>
            </Columns>
            <Popup popupClass={"success-box"} active={successActive} setActive={setSuccessActive} message={"Reset Email Sent!"}/>
            <Popup popupClass={"failure-box"} active={failActive} setActive={setFailActive} message={"Reset Request Failed!"}/>
        </Outline>
    )
}