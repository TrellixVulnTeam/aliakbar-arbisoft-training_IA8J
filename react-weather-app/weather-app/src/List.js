import React from 'react';

const List = props => (
  <ul>
    {
      props.items.map((item) => {
        return(
          <div key={item.city.toString()}>
            {item.country && item.city && <p>Location: {item.city},    {item.country}</p>}
            {item.temperature && <p>Temperature: {item.temperature - 273.15}</p>}
            {item.humidity && <p>Humidity: {item.humidity}</p>}
            {item.description && <p>Conditions:  {item.description}</p>}
            {item.error && <p>{item.error}</p>}
            <p>-----------------------------------------------------------------------------------------------------</p>
          </div>
        )
      })
    }
  </ul>
);

export default List;