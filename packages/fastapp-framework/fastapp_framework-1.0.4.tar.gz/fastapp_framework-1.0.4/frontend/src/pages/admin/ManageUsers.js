import { FaUser } from "react-icons/fa"
import { GrUserAdmin } from "react-icons/gr";
import { IoMdPersonAdd } from "react-icons/io";

import { Column, Columns } from "../../components/Columns"

export default function ManageUsers(props){

    const SelectBox = (props) => {
        return (
            <Column args={'is-4'}>
                <p className="has-text-centered" style={{border: "1px solid", borderRadius: "10px", padding: "20px"}}>
                    <h1 className="title">{props.name}</h1>
                    <a href="/change-view" onClick={(e) => {
                        e.preventDefault();
                        props.setActive(props.viewName);
                    }}>{props.children}</a>
                </p>
            </Column>
        )
    }

    return (
       <Columns>
            <SelectBox name={"View Members"} setActive={props.setActive} viewName={"Members"}><FaUser size={100}/></SelectBox>
            <SelectBox name={"View Admins"} setActive={props.setActive} viewName={"Admins"}><GrUserAdmin size={100}/></SelectBox>
            <SelectBox name={"Add Users"} setActive={props.setActive} viewName={"Add Users"}><IoMdPersonAdd size={100}/></SelectBox>
       </Columns>
    )
}