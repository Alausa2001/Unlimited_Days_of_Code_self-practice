#!/usr/bin/node
const person = {
	  name: ['Bob', 'Smith'],
	  age: 32
};
const input = prompt('Get name or age?')
console.log(person[input])
