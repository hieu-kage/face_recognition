
import React, { useState } from "react";
import {Fragment} from "react";
interface Props{
    items: string[];
    heading: string;
}
const ListGroup =({items,heading}:Props)=> {
    let [selectedIndex, setSelectedIndex] = useState(-1);   
    return (
        <>
            <h1>{heading}</h1>
            {items.length==0 && <p>No item found</p>}
            <ul className="list-group">
                {items.map((item,index)=>
                    <li key={item}
                    className={selectedIndex===index ? "list-group-item active" : "list-group-item"}
                    onClick={()=>setSelectedIndex(index)}
                     >{item}</li>        
                )}
            </ul>
        </>
    ); 
}
export default ListGroup