import { useState } from "react"

import Outline from "../../components/Outline"
import { Column, Columns } from "../../components/Columns"
import { UserMenu } from "../../components/Menu"

import General from "./General"

export default function Profile(props){
    const [activeView, setActiveView] = useState('General')

    const views = {
        'General': <General />
    }

    return(
        <Outline>
            <h2 className="title has-text-centered">Profile</h2>
            <br></br>
            <Columns>
                <Column args={'is-2 ml-2'}>
                    <UserMenu active={activeView} setActive={setActiveView}/>
                </Column>
                <Column args={'ml-4 mr-4'}>
                    {views[activeView]}
                </Column>
            </Columns>
        </Outline>
    )
}