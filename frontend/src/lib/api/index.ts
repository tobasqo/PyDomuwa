import axios from "axios";

export const index = axios.create({
	baseURL: "http://localhost:8080",
	timeout: 5000,
	headers: {
		"Content-Type": "application/json"
	},
});
