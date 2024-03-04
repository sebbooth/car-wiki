import React from "react";
import { useEffect, useState, useMemo, useContext } from "react";
import { SearchContext } from "../../contexts/SearchContext";

import { db } from "../../config/firebase";
import { getDocs, collection } from "firebase/firestore";

import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";

const CarList = () => {
  const [vehicleList, setVehicleList] = useState([]);

  const [headers, setHeaders] = useState(null);
  const [rows, setRows] = useState(null);

  const { searchFields } = useContext(SearchContext);

  const vehiclesCollectionRef = useMemo(() => {
    return collection(db, "testVehicles");
  }, []);

  const getVehicleList = async () => {
    try {
      const data = await getDocs(vehiclesCollectionRef);
      console.log("getVehicleList");
      const filteredData = data.docs.map((doc) => ({
        ...doc.data(),
        id: doc.id,
      }));
      setVehicleList(filteredData);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    getVehicleList();
  }, []);

  const updateTable = () => {
    setHeaders(() => createTableHeaders(searchFields));
    setRows(() => createTableRows(searchFields, vehicleList));
  };

  const createTableHeaders = (searchFields) => {
    const columnGroups = Object.keys(searchFields).map((category) => {
      if (searchFields[category].length != 0) {
        return (
          <TableCell
            key={category}
            align="center"
            colSpan={searchFields[category].length}
          >
            {category}
          </TableCell>
        );
      }
    });

    const columns = Object.keys(searchFields).map((category) => {
      if (searchFields[category].length != 0) {
        const cells = searchFields[category].map((field) => {
          return (
            <TableCell key={field} align="left">
              {field}
            </TableCell>
          );
        });
        return cells;
      }
    });
    return (
      <TableHead>
        <tr>{columnGroups}</tr>
        <tr>{columns}</tr>
      </TableHead>
    );
  };

  const createTableRows = (searchFields, vehicles) => {
    const rows = vehicles.map((vehicle) => {
      const row = Object.keys(searchFields).map((category) => {
        if (searchFields[category].length != 0) {
          const cells = searchFields[category].map((field) => {
            if (category == "General") {
              if (vehicle[field] != undefined) {
                return (
                  <TableCell key={field} align="left">
                    {vehicle[field]}
                  </TableCell>
                );
              } else {
                return (
                  <TableCell key={field} align="left">
                    N/A
                  </TableCell>
                );
              }
            } else {
              if (
                vehicle[category] != undefined &&
                vehicle[category][field] != undefined
              ) {
                return (
                  <TableCell key={field} align="left">
                    {vehicle[category][field]}
                  </TableCell>
                );
              } else {
                return (
                  <TableCell key={field} align="left">
                    N/A
                  </TableCell>
                );
              }
            }
          });
          return cells;
        }
      });
      return <TableRow key={vehicle.id}>{row}</TableRow>;
    });
    return <TableBody>{rows}</TableBody>;
  };

  return (
    <>
      <button onClick={updateTable}>Update</button>
      <Paper sx={{ width: "100%" }}>
        <TableContainer sx={{ maxHeight: 800 }}>
          <Table stickyHeader aria-label="sticky table">
            {headers}
            {rows}
          </Table>
        </TableContainer>
      </Paper>
    </>
  );
};

export default CarList;
