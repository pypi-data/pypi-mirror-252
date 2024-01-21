import {useState} from "react"
import {useCookies} from "react-cookie";
import { ImCross } from "react-icons/im";
import { FaCheck } from "react-icons/fa";



import Outline from "../components/Outline"
import {Column, Columns} from "../components/Columns"

const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
const validateEmail = (email) => email.match(emailRegex);

export default function SignUp(props){
    const [emailActive, setEmailActive] = useState(false);
    const [username, setUsername] = useState('');
    const [first, setFirst] = useState('');
    const [last, setLast] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [passConf, setPassConf] = useState('');
    const [, , ] = useCookies(['fastapp_token']);

    const emailError = email.length > 0 && !validateEmail(email);
    const passwordError = password.length > 0 && (!password.match(/[A-Z]/) || password.length < 8 ||
                          !password.match(/[0-9]/) || !password.match(/[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/));
    const passLength = password.length > 8;
    const passCapital = password.match(/[A-Z]/);
    const passNumber = password.match(/[0-9]/);
    const passSpecial = password.match(/[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/);

    const passConfError = (password.length > 0 || passConf.length > 0) && passConf !== password;
    const invalid = emailError || passwordError || passConfError;

    const doSignup = async () => {
        fetch('/api/v1/auth/signup', {
            method: 'POST',
            body: JSON.stringify({
                name: username,
                first: first,
                last: last,
                email: email,
                password: password
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => {
            if(response.status === 200){
                response.json().then(data => {
                    console.log(data);
                })
            } else {
                response.json().then(data => {
                    console.log(data);
                })
            }
        })
    }

    return (
        <Outline>
            <Columns>
                <Column args={'is-6 is-offset-3'}>
                    <h2 className="title has-text-centered">Fastapp Signup</h2>
                    <form className="form" action="/api/v1/auth/token" method="POST">
                        <div className="field">
                            <label className="label has-text-light">Username</label>
                            <p className="control">
                                <input className='input' placeholder='Ex: timmy123' type='text' name="username"
                                    value={username} onChange={(e) => setUsername(e.target.value)}/>
                            </p>
                        </div>
                        <div className="field">
                            <label className="label has-text-light">Email</label>
                            <p className="control">
                                <input className={`input ${emailError ? 'is-danger': ''}`} placeholder='Ex: timmy@gmail.com' type='email' name="email"
                                    value={email} onChange={(e) => setEmail(e.target.value)}/>
                            </p>
                        </div>
                        <Columns>
                            <Column args={'is-6'}>
                                <div className="field">
                                    <label className="label has-text-light">First Name</label>
                                    <p className="control">
                                        <input className='input' placeholder='Ex: Tim' type='text' name="first"
                                            value={first} onChange={(e) => setFirst(e.target.value)}/>
                                    </p>
                                </div>
                            </Column>
                            <Column args={'is-6'}>
                                <div className="field">
                                    <label className="label has-text-light">Last Name</label>
                                    <p className="control">
                                        <input className='input' placeholder='Ex: Turner' type='text' name="first"
                                            value={last} onChange={(e) => setLast(e.target.value)}/>
                                    </p>
                                </div>
                            </Column>
                        </Columns>
                        <br></br>
                        <div className="field">
                            <label className="label has-text-light">Password</label>
                            <p className="control">
                                <input className={`input ${passwordError ? 'is-danger': ''}`} type='password' name="password"
                                    value={password} onChange={(e) => setPassword(e.target.value)} onFocus={() => setEmailActive(true)}
                                    onBlur={() => {setEmailActive(false)}}/>
                            </p>
                            {emailActive && <p className="mt-2"> 
                                <div>
                                    <span>Passwords must be at least 8 charecters long</span>
                                    {passLength && <span className="ml-2 has-text-success"><FaCheck /></span>}
                                    {!passLength && <span className="ml-2 has-text-danger"><ImCross /></span>}
                                </div>
                                <div>
                                    <span>Passwords must include at least 1 special charecter</span>
                                    {passSpecial && <span className="ml-2 has-text-success"><FaCheck /></span>}
                                    {!passSpecial && <span className="ml-2 has-text-danger"><ImCross /></span>}
                                </div>
                                <div>
                                    <span>Passwords must include at least 1 number</span>
                                    {passNumber && <span className="ml-2 has-text-success"><FaCheck /></span>}
                                    {!passNumber && <span className="ml-2 has-text-danger"><ImCross /></span>}
                                </div>
                                <div>
                                    <span>Passwords must include at least 1 upper case letter</span>
                                    {passCapital && <span className="ml-2 has-text-success"><FaCheck /></span>}
                                    {!passCapital && <span className="ml-2 has-text-danger"><ImCross /></span>}
                                </div> 
                            </p>}
                        </div>
                        <div className="field">
                            <label className="label has-text-light">Confirm Password</label>
                            <div className="control">
                                <input className={`input ${passConfError ? 'is-danger':''}`} type='password' name="password"
                                    value={passConf} onChange={(e) => setPassConf(e.target.value)}/>
                            </div>
                            {passConfError && <p class="help is-danger">Passwords do not match</p>}
                        </div>
                        <div className="field">
                            <button className="button mt-4 is-fullwidth is-success" onClick={(e) => {
                                e.preventDefault();
                                doSignup();
                            }} disabled={invalid}>Login</button>
                        </div>
                    </form>
                </Column>
            </Columns>
        </Outline>
    )
}