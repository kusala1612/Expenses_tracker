package expensemanager.controller;
import expensemanager.entity.Expense;
import expensemanager.entity.Income;
import expensemanager.repository.ExpenseRepository;
import expensemanager.repository.IncomeRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@CrossOrigin("*")
public class BalanceController {

    @Autowired
    private ExpenseRepository expenseRepository;

    @Autowired
    private IncomeRepository incomeRepository;

    @GetMapping("/balance/{userId}")
    public Map<String, Double> balance(
            @PathVariable Long userId){

        double income =
                incomeRepository
                        .findByUserId(userId)
                        .stream()
                        .mapToDouble(
                                Income::getAmount
                        )
                        .sum();

        double expense =
                expenseRepository
                        .findByUserId(userId)
                        .stream()
                        .mapToDouble(
                                Expense::getAmount
                        )
                        .sum();

        Map<String, Double> response =
                new HashMap<>();

        response.put(
                "balance",
                income-expense
        );

        return response;
    }
}