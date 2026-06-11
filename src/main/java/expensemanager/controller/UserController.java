package expensemanager.controller;

import expensemanager.entity.User;
import expensemanager.repository.UserRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@CrossOrigin("*")
public class UserController {

    @Autowired
    private UserRepository userRepository;

    @PostMapping("/register")
    public Map<String,String> register(
            @RequestBody User user){

        Map<String,String> response =
                new HashMap<>();

        Optional<User> existing =
                userRepository.findByUsername(
                        user.getUsername());

        if(existing.isPresent()){

            response.put(
                    "message",
                    "Username already exists.");

            return response;
        }

        userRepository.save(user);

        response.put(
                "message",
                "User registered!");

        return response;
    }

    @PostMapping("/login")
    public Map<String,Object> login(
            @RequestBody User user){

        Map<String,Object> response =
                new HashMap<>();

        Optional<User> dbUser =
                userRepository.findByUsername(
                        user.getUsername());

        if(dbUser.isPresent()
                &&
                dbUser.get()
                        .getPassword()
                        .equals(
                                user.getPassword())){

            response.put(
                    "message",
                    "Login successful!");

            response.put(
                    "user_id",
                    dbUser.get().getId());
        }
        else{

            response.put(
                    "message",
                    "Invalid credentials.");
        }

        return response;
    }
}