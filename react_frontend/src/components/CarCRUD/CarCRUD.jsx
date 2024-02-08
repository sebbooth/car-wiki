import { useEffect, useState, useMemo } from "react";

import { db, auth } from "../../config/firebase";
import {
  getDocs,
  collection,
  addDoc,
  deleteDoc,
  updateDoc,
  doc,
  Timestamp,
} from "firebase/firestore";

import "./Car.scss";

const CarCRUD = () => {
  const [vehicleList, setVehicleList] = useState([]);
  const [newVehicleMake, setNewVehicleMake] = useState("");
  const [newVehicleModel, setNewVehicleModel] = useState("");
  const [newVehicleClass, setNewVehicleClass] = useState([]);
  const [updateVehicleModel, setUpdateVehicleModel] = useState("");

  const vehiclesCollectionRef = useMemo(() => {
    return collection(db, "vehicles");
  }, []);

  const getVehicleList = async () => {
    try {
      const data = await getDocs(vehiclesCollectionRef);
      console.log("getDocs 1");
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

  const onSubmitCar = async () => {
    try {
      await addDoc(vehiclesCollectionRef, {
        make: newVehicleMake,
        model: newVehicleModel,
        class: newVehicleClass,
        dateCreated: new Date(),
        userID: auth?.currentUser?.uid,
      });
      console.log("addDoc 1");
      getVehicleList();
    } catch (err) {
      console.error(err);
    }
  };

  const deleteCar = async (id) => {
    try {
      const vehicleDoc = doc(db, "vehicles", id);
      await deleteDoc(vehicleDoc);

      console.log("deleteDoc 1");
      getVehicleList();
    } catch (err) {
      console.error(err);
    }
  };

  const updateCar = async (id) => {
    try {
      const vehicleDoc = doc(db, "vehicles", id);
      await updateDoc(vehicleDoc, { model: updateVehicleModel });
      console.log("updateDoc 1");
      getVehicleList();
    } catch (err) {
      console.error(err);
    }
  };

  const printDate = (timeStamp) => {
    if (timeStamp) {
      const milliseconds =
        timeStamp.seconds * 1000 + timeStamp.nanoseconds / 1000000;
      const date = new Date(milliseconds);
      return "Date Created: " + date;
    }
    return "";
  };

  const printUser = (uID) => {
    if (uID) {
      return "oh";
    }
    return "";
  };

  return (
    <div>
      <div className="add-car">
        <input
          placeholder="Make..."
          onChange={(e) => setNewVehicleMake(e.target.value)}
        />
        <input
          placeholder="Model..."
          onChange={(e) => setNewVehicleModel(e.target.value)}
        />
        <input
          placeholder="Class(es).."
          onChange={(e) =>
            setNewVehicleClass(
              e.target.value.split(",").map((item) => item.trim())
            )
          }
        />
        <button onClick={onSubmitCar}>Submit Car</button>
      </div>

      <div className="car-list">
        {vehicleList.map((vehicle) => (
          <div className="car-entry" key={vehicle.id}>
            <h4>Make: {vehicle.make}</h4>
            <h4>Model: {vehicle.model}</h4>
            Class(es):
            <ul>
              {vehicle.class.map((vehicleClass) => (
                <li key={vehicleClass}>{vehicleClass}</li>
              ))}
            </ul>
            {printDate(vehicle.dateCreated)}
            {printUser(vehicle.userID)}
            <br />
            <input
              placeholder="update model name..."
              onChange={(e) => setUpdateVehicleModel(e.target.value)}
            />
            <button onClick={() => updateCar(vehicle.id)}>Submit Update</button>
            <br />
            <br />
            <button onClick={() => deleteCar(vehicle.id)}>Delete Car</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CarCRUD;
