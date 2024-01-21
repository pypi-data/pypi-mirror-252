import { useState, useEffect } from 'react'
import { useCookies } from 'react-cookie'

import {Column, Columns} from '../../components/Columns'
import { doAuthFetch } from '../../utils/auth'

const StatBox = (props) => {
    return (
        <Column args={'is-3'}>
            <div className='box has-background-grey'>
                <p className='subtitle has-text-centered'>{props.name}</p>
                <hr></hr>
                <p className='title has-text-centered'>{props.value}</p>
            </div>
        </Column>
    )
}

export default function Dashboard(props){
    const [cookies, , removeCookies] = useCookies(['fastapp_token']);
    const [logins, setLogins] = useState(0);

    useEffect(() => {
        const getLogins = async () => {

            const resp = await doAuthFetch(
                '/api/v1/auth/logins',
                {
                    method: 'GET'
                },
                cookies.fastapp_token,
                removeCookies,
                "/admin"
            )

            if(resp.status === "error"){
                console.error(resp.status)
            } else {
                setLogins(resp.data)
            }
        }

        getLogins();
    }, [cookies.fastapp_token, removeCookies])

    return (
        <div>
            <Columns>
                <StatBox name={'User Logins'} value={logins}/>
                <StatBox name={'Statistic 2'} value={"N/A"}/>
                <StatBox name={'Statistic 3'} value={"N/A"}/>
                <StatBox name={'Statistic 4'} value={"N/A"}/>
            </Columns>
            <div className='box has-background-grey has-text-light'>
                MORE INFO
            </div>
        </div>
    )
}