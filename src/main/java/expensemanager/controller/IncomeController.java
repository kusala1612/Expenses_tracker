package expensemanager.controller;

import expensemanager.entity.Income;
import expensemanager.repository.IncomeRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@CrossOrigin("*")
public class IncomeController {

    @Autowired
    private IncomeRepository incomeRepository;

    @PostMapping("/income")
    public Map<String,String> addIncome(
            @RequestBody Income income){

        incomeRepository.save(income);

        Map<String,String> response =
                new HashMap<>();

        response.put(
                "message",
                "Income added!");

        return response;
    }

    @GetMapping("/income/{userId}")
    public List<Income> getIncome(
            @PathVariable Long userId){

        return incomeRepository
                .findByUserId(userId);
    }
    @GetMapping("/income/total/{userId}")
public Map<String, Double> totalIncome(
        @PathVariable Long userId){

    double total =
            incomeRepository
                    .findByUserId(userId)
                    .stream()
                    .mapToDouble(
                            Income::getAmount
                    )
                    .sum();

    Map<String, Double> response =
            new HashMap<>();

    response.put(
            "total",
            total
    );

    return response;
}
}