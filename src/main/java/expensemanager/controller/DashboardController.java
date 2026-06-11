package expensemanager.controller;

import expensemanager.entity.Expense;
import expensemanager.entity.Income;
import expensemanager.repository.ExpenseRepository;
import expensemanager.repository.IncomeRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@CrossOrigin("*")
public class DashboardController {

    @Autowired
    private ExpenseRepository expenseRepository;

    @Autowired
    private IncomeRepository incomeRepository;

    @GetMapping("/dashboard/{userId}")
    public Map<String,Object> dashboard(
            @PathVariable Long userId){

        List<Expense> expenses =
                expenseRepository.findByUserId(userId);

        List<Income> incomes =
                incomeRepository.findByUserId(userId);

        double totalExpense =
                expenses.stream()
                        .mapToDouble(Expense::getAmount)
                        .sum();

        double totalIncome =
                incomes.stream()
                        .mapToDouble(Income::getAmount)
                        .sum();

        double highestExpense =
                expenses.stream()
                        .mapToDouble(Expense::getAmount)
                        .max()
                        .orElse(0);

        double averageExpense =
                expenses.stream()
                        .mapToDouble(Expense::getAmount)
                        .average()
                        .orElse(0);

        Map<String,Object> result =
                new HashMap<>();

        result.put(
                "totalIncome",
                totalIncome
        );

        result.put(
                "totalExpense",
                totalExpense
        );

        result.put(
                "balance",
                totalIncome-totalExpense
        );

        result.put(
                "highestExpense",
                highestExpense
        );

        result.put(
                "averageExpense",
                averageExpense
        );

        result.put(
                "totalTransactions",
                expenses.size()
        );

        return result;
    }
}