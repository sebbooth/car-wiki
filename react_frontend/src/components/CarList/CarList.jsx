import React from "react";
import { useEffect, useState, useMemo } from "react";

import { db, auth } from "../../config/firebase";
import {
  getDocs,
  collection,
  addDoc,
  deleteDoc,
  updateDoc,
  doc,
  getDoc,
  Timestamp,
} from "firebase/firestore";

import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TablePagination from "@mui/material/TablePagination";
import TableRow from "@mui/material/TableRow";

function createEmptyObjectWithAllFields(collection) {
  const result = {};

  collection.forEach((obj) => {
    addFieldsToResult(obj, result);
  });

  return result;
}

function addFieldsToResult(obj, result) {
  for (const key in obj) {
    if (typeof obj[key] === "object" && obj[key] !== null) {
      if (!result[key] && key != "") {
        result[key] = {};
      }
      addFieldsToResult(obj[key], result[key]);
    } else if (obj[key] !== "") {
      result[key] = null;
    }
  }
}

const CarList = () => {
  const [vehicleList, setVehicleList] = useState([]);
  const [vehicleFields, setVehicleFields] = useState({});

  const vehiclesCollectionRef = useMemo(() => {
    return collection(db, "testVehicles");
  }, []);

  const getVehicleList = async () => {
    try {
      const data = await getDocs(vehiclesCollectionRef);
      console.log("getDocs");
      const filteredData = data.docs.map((doc) => ({
        ...doc.data(),
        id: doc.id,
      }));
      setVehicleList(filteredData);
      let fields = createEmptyObjectWithAllFields(filteredData);
      delete fields["URL"];
      delete fields["userID"];
      delete fields["dateCreated"];
      delete fields["imgURL"];
      delete fields["id"];
      setVehicleFields(fields);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    getVehicleList();
  }, []);

  const createTableHeaders = (obj) => {
    const columnGroups = Object.keys(obj).map((key) => {
      if (typeof obj[key] === "object" && obj[key] !== null) {
        return (
          <TableCell
            key={key}
            align="center"
            colSpan={Object.keys(obj[key]).length}
          >
            {key}
          </TableCell>
        );
      } else {
        return (
          <TableCell key={key} align="center" colSpan={1}>
            {key}
          </TableCell>
        );
      }
    });

    const columns = Object.keys(obj).map((key) => {
      if (typeof obj[key] === "object" && obj[key] !== null) {
        return Object.keys(obj[key]).map((subKey) => (
          <TableCell key={subKey} align="left">
            {subKey}
          </TableCell>
        ));
      } else {
        return (
          <TableCell key={key} align="left">
            {key}
          </TableCell>
        );
      }
    });

    return (
      <TableHead>
        <tr>{columnGroups}</tr>
        <tr>{columns}</tr>
      </TableHead>
    );
  };

  const createTableRows = (obj, vehicles) => {
    const rows = vehicles.map((vehicle) => {
      const row = Object.keys(obj).map((key) => {
        if (typeof obj[key] === "object" && obj[key] !== null) {
          return Object.keys(obj[key]).map((subKey) => {
            if (
              vehicle[key] != undefined &&
              vehicle[key][subKey] != undefined
            ) {
              return (
                <TableCell key={subKey} align="left">
                  {vehicle[key][subKey]}
                </TableCell>
              );
            } else {
              return (
                <TableCell key={subKey} align="left">
                  N/A
                </TableCell>
              );
            }
          });
        } else {
          if (vehicle[key] != undefined) {
            return (
              <TableCell key={key} align="left">
                {vehicle[key]}
              </TableCell>
            );
          } else {
            return (
              <TableCell key={key} align="left">
                N/A
              </TableCell>
            );
          }
        }
      });
      return <TableRow key={vehicle.id}>{row}</TableRow>;
    });
    return <TableBody>{rows}</TableBody>;
  };

  return (
    <Paper sx={{ width: "100%" }}>
      <TableContainer sx={{ maxHeight: 800 }}>
        <Table stickyHeader aria-label="sticky table">
          {createTableHeaders(vehicleFields)}
          {createTableRows(vehicleFields, vehicleList)}
        </Table>
      </TableContainer>
    </Paper>
  );
};

export default CarList;
