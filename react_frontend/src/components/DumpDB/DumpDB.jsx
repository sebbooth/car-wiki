import React from "react";
import { useMemo } from "react";
import { db, auth } from "../../config/firebase";
import {
  collection,
  addDoc,
  query,
  where,
  doc,
  updateDoc,
  getCountFromServer,
} from "firebase/firestore";

import rawData from "../../../../data_mine/selenium/wikipedia/output/vehicles.json";

function getRandomItemsFromArray(array, numItems) {
  const randomItemsArray = [];
  const arrayLength = array.length;
  const selectedIndices = new Set();

  while (randomItemsArray.length < numItems) {
    const randomIndex = Math.floor(Math.random() * arrayLength);
    if (!selectedIndices.has(randomIndex)) {
      randomItemsArray.push(array[randomIndex]);
      selectedIndices.add(randomIndex);
    }
  }

  return randomItemsArray;
}

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

const DumpDB = () => {
  //const data = getRandomItemsFromArray(rawData, 30);

  //const emptyObjectWithAllFields = createEmptyObjectWithAllFields(rawData);
  //console.log(emptyObjectWithAllFields);
  const vehiclesCollectionRef = useMemo(() => {
    return collection(db, "testVehicles");
  }, []);

  const submitCar = async (vehicle) => {
    console.log(vehicle.Make, vehicle.Model);
    const q = query(
      vehiclesCollectionRef,
      where("Make", "==", vehicle.Make),
      where("Model", "==", vehicle.Model)
    );

    const snapshot = await getCountFromServer(q);
    if (snapshot.data().count == 0) {
      vehicle.dateCreated = new Date();
      vehicle.userID = auth?.currentUser?.uid;
      try {
        await addDoc(vehiclesCollectionRef, {
          ...vehicle,
        });
        console.log("add ", vehicle.Make, vehicle.Model);
      } catch (err) {
        console.error(err);
      }
    }
  };

  const dumpFields = async () => {
    try {
      const vehicleDoc = doc(db, "testVehicles", "allFields");
      await updateDoc(vehicleDoc, { ...emptyObjectWithAllFields });
      console.log("updateDoc");
    } catch (err) {
      console.error(err);
    }
  };

  const onClick = () => {
    data.map((item) => {
      submitCar(item);
    });
  };

  const testQuery = async () => {
    const q = query(vehiclesCollectionRef, where("Make", "==", "Dodge"));

    const snapshot = await getCountFromServer(q);
    console.log(q);
    console.log(snapshot.data());
  };

  return (
    <div>
      <button
        onClick={() => {
          console.log(data);
        }}
      >
        Print data
      </button>
      <button onClick={testQuery}>Test query</button>
      <button onClick={onClick}>Dump data</button>
      <button onClick={dumpFields}>Dump fields</button>
    </div>
  );
};

export default DumpDB;
