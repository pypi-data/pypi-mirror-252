import { useState, useEffect } from 'react';
import { useCookies } from "react-cookie";
import { MdDelete } from "react-icons/md";

import {Column, Columns} from "../../components/Columns"
import { doAuthFetch } from "../../utils/auth"

const PAGESIZE = 10;

export default function Members(props){
    const [users, setUsers] = useState([]);
    const [count, setCount] = useState(0);
    const [page, setPage] = useState(1);
    const [search, setSearch] = useState('');
    const [reload, setReload] = useState(false);
    const [cookies, , removeCookies] = useCookies(['fastapp_token']);

    const doDeleteUser = async (username) => {
        const resp = await doAuthFetch(
            `/api/v1/auth/user`,
            {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: username
                })
            },
            cookies.fastapp_token,
            removeCookies,
            "/admin"
        )

        if(resp.status === "success"){
            setReload(!reload);
            console.log(resp);
        }
    };

    useEffect(() => {
        const fetchMembers = async () => {
            var params = new URLSearchParams({
                is_admin: props.is_admin,
                skip: (page-1)*PAGESIZE,
                limit: PAGESIZE
            })

            if(search !== ''){
                params.append('search', search);
            }

            const resp = await doAuthFetch(
                '/api/v1/auth/users?' + params,
                {
                    method: "GET"
                },
                cookies.fastapp_token,
                removeCookies,
                "/admin"
            )

            if(resp.status === "success"){
                setUsers(resp.data.users);
                setCount(Math.ceil(resp.data.count / PAGESIZE));
            }
        }

        fetchMembers()
    }, [cookies.fastapp_token, removeCookies, props.is_admin, reload, page, search]);

    return (
        <div>
            <Columns>
                <Column args={'is-4'}>
                    <div className='level'>
                        <div className='level-item is-size-4'>
                            Search
                        </div>
                        <div className='level-item'>
                            <input className='input has-background-dark has-text-light mb-1'
                                placeholder='Search' type='text' value={search} onChange={(e) => {
                                    e.preventDefault();
                                    setSearch(e.target.value);
                                }}>
                            </input>
                        </div>
                    </div>
                </Column>
                <Column args={'is-4'}>
                    <h1 className='title has-text-centered'>Members</h1>
                </Column>
                <Column args={'is-4'}>
                </Column>
            </Columns>
            <table className="table is-fullwidth has-background-dark is-bordered">
                <thead>
                    <tr>
                        <th className='has-text-light'>Username</th>
                        <th className='has-text-light'>Email</th>
                        <th className='has-text-light'>Active</th>
                        <th className='has-text-light'>Admin</th>
                        <th className='has-text-light'>Delete</th>
                    </tr>
                </thead>
                <tbody>
                    { users.map !== undefined && users.map((value, index) => {
                    return (
                        <tr key={index}>
                            <td className='has-text-light'>{value.name}</td>
                            <td className='has-text-light'>{value.email}</td>
                            <td className='has-text-light'>{value.is_active ? 'Yes': 'No'}</td>
                            <td className='has-text-light'>{value.is_admin ? 'Yes' : 'No'}</td>
                            <th className='has-text-light'>
                                <a href='/user/delete' onClick={(e) => {
                                    e.preventDefault();
                                    if(window.confirm(`Are you sure you want to delete '${value.name}'`))
                                        doDeleteUser(value.name);
                                }}><MdDelete /></a>
                            </th>
                        </tr>
                    )
                    })}
                </tbody>
            </table>
            <nav class="pagination is-centered" role="navigation" aria-label="pagination">
                <a class="pagination-previous" onClick={(e) => {
                    e.preventDefault();
                    if(page > 1)
                        setPage(page - 1);
                }} href='/next-page'>Previous</a>
                <a class="pagination-next" onClick={(e) => {
                    e.preventDefault();
                    if(page < count)
                        setPage(page + 1);
                }} href='/next-page'>Next page</a>
                <ul class="pagination-list">
                    {(page !== 1) && <li><a class="pagination-link" aria-label="Goto page 1" onClick={(e) => {
                        e.preventDefault();
                        setPage(1);
                    }}>1</a></li>}
                    {(page !== 1) && <li><span class="pagination-ellipsis">&hellip;</span></li>}
                    {(page - 2 > 0) && <li><a class="pagination-link" aria-label={`Goto page ${page-1}`} onClick={(e) => {
                        e.preventDefault();
                        setPage(page - 1);
                    }}>{page-1}</a></li>}
                    <li><a class="pagination-link is-current" aria-label={`Page ${page}`} aria-current="page">{page}</a></li>
                    {(page + 2 <= count) && <li><a class="pagination-link" aria-label="Goto page 47" onClick={(e) => {
                        e.preventDefault();
                        setPage(page + 1);
                    }}>{page + 1}</a></li>}
                    {(page < count) && <li><span class="pagination-ellipsis">&hellip;</span></li>}
                    {(page < count) && <li><a class="pagination-link" aria-label={`Goto page ${count}`} onClick={(e) => {
                        e.preventDefault();
                        setPage(count);
                    }}>{count}</a></li>}
                </ul>
            </nav>
        </div>
    )
}